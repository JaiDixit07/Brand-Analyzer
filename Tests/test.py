import os
from dotenv import load_dotenv
import tweepy

load_dotenv()

bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
client = tweepy.Client(bearer_token=bearer_token)

try:
    tweets = client.search_recent_tweets(query="python", max_results=10)
    if tweets.data:
        for tweet in tweets.data:
            print(tweet.text)
    else:
        print("No tweets found")
except Exception as e:
    print(f"Error: {e}")