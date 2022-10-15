#!/usr/bin/env python
import logging
import os
import sys
from pathlib import Path
import json
from dotenv import load_dotenv
import tweepy

load_dotenv()

# Your app's bearer token can be found under the Authentication Tokens section
# of the Keys and Tokens tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")


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
        "(@apachekafka OR @ApacheAirflow OR @cassandra OR @apachesuperset OR @ClickHouseDB)",
    )
    return_json = {"return_value": tweets}

    Path("./airflow/xcom").mkdir(parents=True, exist_ok=True)
    # write to the file checked by Airflow for XComs
    f = open('./airflow/xcom/return.json', 'w')
    f.write(f"{json.dumps(return_json)}")
    f.close()


def read_xcom_tweets():
    with open('./airflow/xcom/return.json', 'r') as f:
        data = json.load(f)

    print(data)


def main():
    # You can authenticate as your app with just your bearer token
    client = tweepy.Client(bearer_token=bearer_token)
    save_data_to_file(client)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())
