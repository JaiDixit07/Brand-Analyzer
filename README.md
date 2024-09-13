# Brand Analyzer

Brand Analyzer is a sentiment analysis application designed to analyze Twitter data related to a specific brand. It collects tweets using the `ntscraper` library, preprocesses them (removing links, mentions, and other noise), and then uses a fine-tuned RoBERTa model to predict the sentiment of the tweets. The model classifies emotions like anger, disgust, fear, joy, sadness, surprise, and neutral, mapping them to either positive or negative sentiments.

The app also provides recommendations based on the predominant sentiment, helping brands improve in areas such as customer service, product quality, pricing, and marketing.

[Watch the video demo here](https://youtu.be/WUqAg3zj-MQ)


## 🚀 Features

- **Web Scraping**: Scrapes tweets from the internet related to a specific brand using `ntscraper`.
- Preprocesses the tweets (removes URLs, mentions, hashtags, etc.).
- Translates tweets to English if necessary using `deep_translator`.
- **Transformers**: Uses a `Hugging Face` pre-trained `RoBERTa model` for sentiment analysis.
- Provides recommendations based on the predominant sentiment.
- **Secure API Access & Flask**: `Flask` web application with a user-friendly API.

## 🏗️ Project Structure

- **`data/`**: Raw and cleaned data files.
- **`Templates/`**: HTML templates for the Flask application’s front end.
- **`app/`**: Flask app setup for serving the model and interface.
- **`static/`**: CSS file for styling and JS file.
- **`requirements/`**: All the necessary libraries
- **`sentiment.ipynb`**: Python notebook for training model and fine-tuning parameters.

## 🔍 Data

The dataset used is featuring:
- Index
- Tweets
- Sentiment

## 💻 Installation

### Clone the Repository

```bash
git clone https://github.com/JaiDixit07/Brand-Analyzer.git
cd Brand-Analyzer
```

Install Dependencies
Ensure you have Python 3.8+ installed, then install the required Python packages with:

```bash
pip install -r requirements.txt
```


##  Required Libraries

- pandas
- numpy
- matplotlib 
- scikit-learn
- torch
- transformers
- flask
- deep_translator
- python-dotenv
- gunicorn`(For deployment purpose)` 
- ntscraper

# 🖥️ Usage
To run the application locally:

Clone the repository and install dependencies.
Run the Flask app:
```bash
python app.py
```
The app will be available at http://localhost:5000. From there, you can input the brand you want to analyze and get the desired analysis

## Model and Tokenizer

The model and tokenizer are hosted on Hugging Face Hub:

- **Model :** `jaidixit07/brand_model`
- **Tokenizer :** `jaidixit07/brand_token`

## 🤝 Contributions
Contributions are welcome! Feel free to fork the repository, submit issues, or create pull requests.

## 📝 License
This project is licensed under the MIT License. See the LICENSE file for more details.

## 🙌 Acknowledgements
- **ntscraper** for providing the necessary web scraping instance used in analysis.
- **Flask** for the web framework powering the user interface.
- **Hugging Face** for hosting the trained model and token and the pre trained roBERTa model.

-------------------------------------------------------------------------------------------------

Developed by Jai Dixit.