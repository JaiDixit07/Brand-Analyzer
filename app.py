from flask import Flask, request, render_template, jsonify
from ntscraper import Nitter
import pandas as pd
import re
from deep_translator import GoogleTranslator
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from os import environ
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load model from Hugging Face Hub
model_name = "jaidixit07/brand_model"
token_name="jaidixit07/brand_token"
tokenizer = AutoTokenizer.from_pretrained(token_name, use_auth_token=environ.get("HF_TOKEN"))
model = AutoModelForSequenceClassification.from_pretrained(model_name, use_auth_token=environ.get("HF_TOKEN"))

# Nitter instances
NITTER_INSTANCES = [
    # many instances Ignore this I will add them later 
]


def translate_to_english(text, source_language='auto'):
    translator = GoogleTranslator(source=source_language, target='en')
    translation = translator.translate(text)
    return translation

def lowercase_text(text):
    if isinstance(text, str):
        return text.lower()
    else:
        # If the input is not a string (e.g., float or non-string), return it unchanged
        return text
    

def remove_com_links(text):
    # Define a regular expression pattern to match ".com" and everything before and after it until a space
    pattern = r'\S*\.com\S*'
    
    # Use re.sub to replace the matched pattern with an empty string
    cleaned_text = re.sub(pattern, '', text)
    
    return cleaned_text


def remove_html_tags(text):
    if isinstance(text, str):
        clean_text = re.sub(r'<.*?>', ' ', text)
        return clean_text
    else:
        return text
    

def remove_urls(text):
    if isinstance(text, str):
        # Remove any URL starting with "http://" or "https://"
        clean_text = re.sub(r'http\S+|www\S+', ' ', text)
        return clean_text
    else:
        return text
        
def remove_hashtags(text):
     if isinstance(text, str):
        return re.sub(r'#', ' ', text)
     else:
        # If the input is not a string (e.g., float or non-string), return it unchanged
        return text

    

# Remove mentions
def remove_mentions(text):
     if isinstance(text, str):
        return re.sub(r'@\w+', ' ', text)
     else:
        # If the input is not a string (e.g., float or non-string), return it unchanged
        return text

def convert_emojis(text):
    # Emoji mapping
    if isinstance(text, str):
        # Replace emojis with their text representations
        for emoji in emoji_mapping:
            text = text.replace(emoji, emoji_mapping[emoji])
        return text
    else:
        # If the input is not a string (e.g., float or non-string), return it unchanged
        return text

def convert_emoticons(text):
    # Emoticon mapping
     if isinstance(text, str):
        # Replace emojis with their text representations
        for emoticon in emoticon_mapping:
            text = text.replace(emoticon, emoticon_mapping[emoticon])
        return text
     else:
        # If the input is not a string (e.g., float or non-string), return it unchanged
        return text



emoticon_mapping = {
 '(:': 'Happy ',
 ':‑)': 'Happy ',
 ':-))': 'Very happy ',
 ':-)))': 'Very very Happy ',
 ':)': 'smiley ',
 ':))': 'Very smiley ',
 ':)))': 'Very very smiley ',
 ':-]': 'smiley ',
 ':]': 'Happy ',
 ':-3': 'smiley ',
 ':3': 'Happy ',
 ':->': 'smiley ',
 ':>': 'Happy ',
 '8-)': 'smiley ',
 ':o)': 'Happy ',
 ':-}': 'smiley ',
 ':}': 'Happy ',
 ':-)': 'smiley ',
 ':c)': 'Happy ',
 ':^)': 'smiley ',
 '=]': 'Happy ',
 '=)': 'smiley ',
 ':‑D': 'Laughing ',
 ':D': 'Laughing ',
 '8‑D': 'Laughing ',
 '8D': 'big grin ',
 'X‑D': 'big grin ',
 'XD': 'big grin ',
 '=D': 'laugh ',
 '=3': 'laugh ',
 'B^D': 'laugh ',
 ':-(': 'Frown ',
 ':‑(': 'Frown ',
 ':(': 'sad ',
 ':‑c': 'sad ',
 ':c': 'andry ',
 ':‑<': 'andry ',
 ':<': 'pouting ',
 ':‑[': 'pouting ',
 ':[': 'Frown ',
 ':-||': 'Frown ',
 '>:[': 'sad ',
 ':{': 'andry ',
 ':@': 'pouting ',
 '>:(': 'Frown ',
 ":'‑(": 'Crying ',
 ":'(": 'Crying ',
 ":'‑)": 'happiness ',
 ":')": 'happiness',
 "D‑':": 'Horror ',
 'D:<': 'Disgust ',
 'D:': 'Sadness ',
 'D8': 'dismay ',
 'D;': 'dismay ',
 'D=': 'dismay ',
 'DX': 'dismay ',
 ':‑O': 'Surprise ',
 ':O': 'Surprise ',
 ':‑o': 'Surprise ',
 ':o': 'Surprise ',
 ':-0': 'Shock ',
 '8‑0': 'Yawn ',
 '>:O': 'Yawn ',
 ':-*': 'Kiss ',
 ':*': 'Kiss ',
 ':X': 'Kiss ',
 ';‑)': 'Wink ',
 ';)': 'smirk ',
 '*-)': 'Wink ',
 '*)': 'smirk ',
 ';‑]': 'Wink ',
 ';]': 'smirk ',
 ';^)': 'Wink ',
 ':‑,': 'smirk ',
 ';D': 'Wink ',
 ':‑P': 'cheeky ',
 ':P': 'cheeky ',
 'X‑P': 'playful ',
 'XP': 'cheeky ',
 ':‑Þ': 'cheeky ',
 ':Þ': 'cheeky ',
 ':b': 'playful ',
 'd:': 'playful ',
 '=p': 'playful ',
 '>:P': 'playful ',
 ':‑/': 'Skeptical ',
 ':/': 'Skeptical ',
 ':-[.]': 'annoyed ',
 '>:[(\\)]': 'annoyed ',
 '>:/': 'undecided ',
 ':[(\\)]': 'undecided ',
 '=/': 'uneasy ',
 '=[(\\)]': 'uneasy ',
 ':L': 'hesitant ',
 '=L': 'hesitant ',
 ':S': 'Skeptical ',
 ':‑|': 'no expression ',
 ':|': 'indecision ',
 ':$': 'Embarrassed or blushing ',
 ':‑x': 'Sealed lips ',
 ':x': 'tongue-tied ',
 ':‑#': 'Sealed lips ',
 ':#': 'tongue-tied ',
 ':‑&': 'Sealed lips ',
 ':&': 'tongue-tied ',
 'O:‑)': 'Angel ',
 'O:)': 'innocent ',
 '0:‑3': 'Angel ',
 '0:3': 'innocent ',
 '0:‑)': 'Angel ',
 '0:)': 'innocent ',
 ':‑b': 'playful ',
 '0;^)': 'Angel ',
 '>:‑)': 'Evil ',
 '>:)': 'devilish ',
 '}:‑)': 'Evil ',
 '}:)': 'devilish ',
 '3:‑)': 'Evil ',
 '3:)': 'devilish ',
 '>;)': 'Evil ',
 '|;‑)': 'Cool ',
 '|‑O': 'Bored ',
 ':‑J': 'contempt ',
 '%‑)': 'Drunk ',
 '%)': 'confused ',
 ':-###..': 'sick ',
 ':###..': 'sick ',
 '<:‑|': 'Dump ',
 '(>_<)': 'Troubled ',
 '(>_<)>': 'Troubled ',
 "(';')": 'Baby ',
 '(^^>``': 'Nervous ',
 '(^_^;)': 'Embarrassed ',
 '(-_-;)': 'Troubled ',
 '(~_~;) (・.・;)': 'Shyp ',
 '(-_-)zzz': 'Sleeping ',
 '(^_-)': 'Wink ',
 '((+_+))': 'Confused ',
 '(+o+)': 'Confused ',
 '(o|o)': 'Ultraman ',
 '^_^': 'Joyful ',
 '(^_^)/': 'Joyful ',
 '(^O^)／': 'Joyful ',
 '(^o^)／': 'Joyful ',
 '(__)': 'respect ',
 '_(._.)_': 'apology ',
 '<(_ _)>': 'respect ',
 '<m(__)m>': 'apology ',
 'm(__)m': 'respect ',
 'm(_ _)m': 'apology ',
 "('_')": 'Sad ',
 '(/_;)': 'Crying ',
 '(T_T) (;_;)': 'Sad ',
 '(;_;': 'Crying ',
 '(;_:)': 'Sad ',
 '(;O;)': 'Crying ',
 '(:_;)': 'Sad ',
 '(ToT)': 'Crying ',
 ';_;': 'Sad ',
 ';-;': 'Crying ',
 ';n;': 'Sad ',
 ';;': 'Crying ',
 'Q.Q': 'Sad ',
 'T.T': 'Crying ',
 'QQ': 'Sad ',
 'Q_Q': 'Crying ',
 '(-.-)': 'Shame ',
 '(-_-)': 'Shame ',
 '(一一)': 'Shame ',
 '(；一_一)': 'Shame ',
 '(=_=)': 'Tired ',
 '(=^·^=)': 'cat ',
 '(=^··^=)': 'cat ',
 '=_^= ': 'cat ',
 '(..)': 'sadness ',
 '(._.)': 'boredom ',
 '^m^': 'Giggling ',
 '(・・?': 'Confusion ',
 '(?_?)': 'Confusion ',
 '>^_^<': 'Laugh ',
 '<^!^>': 'Laugh ',
 '^/^': 'Laugh ',
 '（*^_^*）': 'Laugh ',
 '(^<^) (^.^)': 'Laugh ',
 '(^^)': 'Laugh ',
 '(^.^)': 'Laugh ',
 '(^_^.)': 'Laugh ',
 '(^_^)': 'Laugh ',
 '(^J^)': 'Laugh ',
 '(*^.^*)': 'Laugh ',
 '(^—^）': 'Laugh ',
 '(#^.^#)': 'Laugh ',
 '（^—^）': 'Waving ',
 '(;_;)/~~~': 'Waving ',
 '(^.^)/~~~': 'Waving ',
 '(-_-)/~~~ ($··)/~~~': 'Waving ',
 '(T_T)/~~~': 'Waving ',
 '(ToT)/~~~': 'Waving ',
 '(*^0^*)': 'Excited ',
 '(*_*)': 'Amazed ',
 '(*_*;': 'Amazed ',
 '(+_+) (@_@)': 'Amazed ',
 '(*^^)v': 'Laughing ',
 '(^_^)v': 'Cheerful ',
 '((d[-_-]b))': 'Headphones ',
 '(-"-)': 'Worried ',
 '(ーー;)': 'Worried ',
 '(^0_0^)': 'win ',
 '(＾ｖ＾)': 'Happy ',
 '(＾ｕ＾)': 'Happy ',
 '(^)o(^)': 'Happy ',
 '(^O^)': 'Happy ',
 '(^o^)': 'Happy ',
 ')^o^(': 'Happy ',
 ':O o_O': 'Surprised ',
 'o_0': 'Surprised ',
 'o.O': 'Surpised ',
 '(o.o)': 'Surprised ',
 'oO': 'Surprised ',
 '(*￣m￣)': 'Dissatisfied ',
 '(‘A`)': 'Deflated ',
  '*-*':'In Love ',
  '^^':'happy ',
  'c:':'bummed',
  '( ´ ▽ ` )ﾉ':"happy",
  '(:':'smile',
   '>.<':'annoyed',
   '-_-':'neutral'
     
}

# emoji mapping
emoji_mapping = {
    '🙂':'Smiley ',
    '😊':'happy ',
    '😀':'Smiley ',
    '😁':'happy ',
    '😃':'Laughing ',
    '😄':'big grin ',
    '😆':'Laughing ',
    '😂':'Laughing ',
    '🤒':'sick ',
    '😛':'playful ',
    '☹️':'Frown ',
    '🙁':'sad ',
    '😔':'sad ',
    '😞':'pouting ',
    '😟':'Frown ',
    '😣':'annoyed ',
    '😖':'hesitant ',
    '😢':'Crying ',
    '😭':'Crying ',
    '🥺':'crying ',
    '😠':'Angry ',
    '😡':'Angry ',
    '😨':'Horror ',
    '😧':'Horror ',
    '😱':'Shocked ',
    '😫':'sadness ',
    '😩':'dismay ',
    '😦':'sadness ',
    '😮':'Surprise ',
    '😯':'Surprise ',
    '😲':'shock ',
    '😗':'Kiss ',
    '😙':'Kiss ',
    '😚':'Kiss',
    '😘':'Kiss ',
    '😍':'love ',
    '😉':'Wink ',
    '😜':'smirk ',
    '😝':'cheeky ',
    '😜':'playful ',
    '🤑':'money ',
    '😐':'no expression ',
    '😑':'indecision ',
    '😳':'Embarrassed ',
    '🤐':'Sealed lips ',
    '😶':'tongue tied ',
    '😇':'Angel ',
    '👼':'innocent ',
    '😈':'Evil ',
    '😎':'Cool ',
    '😪':'bored ',
    '😏':'disdain ',
    '😒':'disdain ',
    '😕':'confused ',
    '😵‍':'Drunk ',
    '🤕':'confused ',
    '🤒':'sick ',
    '😷':'sick ',
    '🤢':'disgust ',
    '🤨':'Scepticism ',
    '😬':'Grimacing ',
    '☠️':'dangerous ',
    '💀':'grave ',
    '🌹':'love ',
    '❤️':'love ',
    '💔':'sad ',
    '🍻':'Cheer ',
    '👶':'Baby ',
    '😅':'troubled ',
    '😓':'disappointed ',
    '😴':'Sleeping ',
    '💤':'Sleeping ',
    '🙄':'Confused ',
    '🙌':'Joyful ',
    '🙇':'apology ',
    '💃':'Excited ',
    '🤷':'shrug ',
}

emo_mapper = {
    'angry': 'negative',
    'sadness': 'negative',
    'disgust': 'negative',
    'fear': 'negative',
    'joy': 'positive',
    'surprise': 'positive',
    'neutral': 'positive'
}

def get_posts(brand, instance_index=0):
    query = str(brand)
    scraper = Nitter()
    
    try:
        tweets = scraper.get_tweets(query, mode='hashtag', number=50)
    except Exception as e:
        if instance_index < len(NITTER_INSTANCES) - 1:
            return get_posts(brand, instance_index + 1)
        else:
            raise Exception("All Nitter instances failed")

    text = [tweet['text'] for tweet in tweets['tweets']]
    df = pd.DataFrame({'text': text})
    
    # Apply preprocessing functions
    for func in [translate_to_english, remove_urls, remove_com_links, convert_emojis, 
                 convert_emoticons, remove_mentions, remove_hashtags, remove_html_tags, lowercase_text]:
        df['text'] = df['text'].apply(func)
    
    return df

def get_predictions(data):
    inputs = tokenizer(data['text'].tolist(), padding=True, truncation=True, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_classes = torch.argmax(predictions, dim=-1).tolist()
    
    labels = {0: 'anger', 1: 'disgust', 2: 'fear', 3: 'joy', 4: 'neutral', 5: 'sadness', 6: 'surprise'}
    emo_mapper = {'anger': 'negative', 'sadness': 'negative', 'disgust': 'negative', 'fear': 'negative',
                  'joy': 'positive', 'surprise': 'positive', 'neutral': 'positive'}
    
    data['predicted_label'] = [labels[pred] for pred in predicted_classes]
    data['sentiment'] = data['predicted_label'].map(emo_mapper)
    
    emo_percentage = data.predicted_label.value_counts()
    sentiment = data.sentiment.value_counts().index[0]
    
    recom = get_recommendations(sentiment)
    
    # Convert int64 to standard Python int for JSON serialization
    emo_dict = {k: int(v) for k, v in emo_percentage.items()}
    sample_tweet = data.text.sample(1).iloc[0]
    
    return {'emo_dict': emo_dict, 'recom': recom, 'sample_tweet': sample_tweet}

def get_recommendations(sentiment):
    recom = {}
    if sentiment == "positive":
        recom["Customer Service"] = "Maintain excellent service. Personalize interactions and exceed expectations."
        recom["Product Quality"] = "Uphold high standards. Use feedback for continuous improvement."
        recom["Price"] = "Offer competitive pricing and loyalty rewards."
        recom["Marketing"] = "Highlight positive customer experiences in campaigns."
    else:
        recom["Customer Service"] = "Address concerns promptly. Listen, apologize, and provide solutions."
        recom["Product Quality"] = "Implement strict quality control. Offer replacements for defective items."
        recom["Price"] = "Ensure transparent pricing. Consider flexible payment options."
        recom["Marketing"] = "Use feedback constructively. Emphasize improvements in messaging."
    return recom

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    brand = data.get('brand')
    try:
        tweets_data = get_posts(brand)
        response = get_predictions(tweets_data)
        return jsonify({'success': True, 'data': response})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False)