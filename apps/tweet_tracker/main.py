#!/usr/bin/env python
import logging
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
import tweepy
import pandas as pd

load_dotenv()

# Your app's bearer token can be found under the Authentication Tokens section
# of the Keys and Tokens tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps
bearer_token = os.getenv("BEARER_TOKEN")


def extract_recent_tweets_raw(client: tweepy.Client, arg: str):
    # Search Recent Tweets

    # This endpoint/method returns Tweets from the last seven days

    response = client.search_recent_tweets(
        f"{arg} -is:retweet -is:reply",
        max_results=100,
        tweet_fields=['created_at', 'text', 'source', 'lang'],
    )
    # In this case, the data field of the Response returned is a list of Tweet
    # objects
    tweets = response.data
    # Each Tweet object has default ID and text fields
    return [{
        "id": tweet.data.get("id"),
        "text": tweet.data.get("text"),
        "created": tweet.data.get("created_at"),
        "lang": tweet.data.get("lang"),
        "source": tweet.data.get("source")
    } for tweet in tweets]


def save_data_to_file(client: tweepy.Client, ):
    tweets = extract_recent_tweets_raw(
        client,
        "(@apachekafka OR @ApacheAirflow OR @cassandra OR @apachesuperset)",
    )
    print(tweets[0:1])
    df = pd.DataFrame(tweets)
    df.to_json("./tweet.json", orient='records')


def main():
    # You can authenticate as your app with just your bearer token
    client = tweepy.Client(bearer_token=bearer_token)
    save_data_to_file()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
