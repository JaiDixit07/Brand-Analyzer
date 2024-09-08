from flask import Flask, request, render_template, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import pandas as pd
import re
from deep_translator import GoogleTranslator
import time
from concurrent.futures import ThreadPoolExecutor
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# HuggingFace setup
hf_token = os.getenv('HF_TOKEN')
model_name = "jaidixit07/brand_model"
token_name = "jaidixit07/brand_token"

tokenizer = AutoTokenizer.from_pretrained(token_name, token=hf_token)
model = AutoModelForSequenceClassification.from_pretrained(model_name, token=hf_token)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# Twitter API setup
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
client = tweepy.Client(bearer_token=bearer_token)

def translate_to_english(text, source_language='auto'):
    try:
        translator = GoogleTranslator(source=source_language, target='en')
        return translator.translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def preprocess_text(text):
    text = re.sub(r'http\S+|www\S+|@\w+|#\w+', '', text)
    text = re.sub(r'<.*?>', '', text)
    return text.lower()

def get_posts(brand, max_results=50):
    tweets = []
    for tweet in tweepy.Paginator(client.search_recent_tweets, 
                                  query=brand, 
                                  max_results=10).flatten(limit=max_results):
        tweets.append({'text': tweet.text})
    
    df = pd.DataFrame(tweets)
    
    if df.empty:
        print(f"No tweets found for {brand}")
        return pd.DataFrame(columns=['text'])
    
    # Translate and preprocess tweets using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        df['text'] = list(executor.map(lambda x: translate_to_english(x) if x else '', df['text']))
    
    # Preprocess the text
    df['text'] = df['text'].apply(preprocess_text)
    
    return df


def get_predictions(data):
    if data.empty:
        return {
            'emo_dict': {},
            'sample_tweet': "No tweets available for analysis."
        }

    inputs = tokenizer(data['text'].tolist(), padding=True, truncation=True, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_classes = torch.argmax(predictions, dim=-1).cpu().tolist()
    
    labels = ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise']
    data['predicted_label'] = [labels[i] for i in predicted_classes]
    
    emo_percentage = data.predicted_label.value_counts(normalize=True) * 100
    
    return {
        'emo_dict': emo_percentage.to_dict(),
        'sample_tweet': data.text.sample(1).iloc[0] if not data.empty else "No sample tweet available."
    }

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    brand = data.get('brand')
    
    posts = get_posts(brand)
    results = get_predictions(posts)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)