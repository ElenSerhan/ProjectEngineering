# 04/03/2020
# Alan Serhan
# g00349187@gmit.ie
# https://github.com/ElenSerhan/ProjectEngineering/

from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob

import numpy as np
import pandas as pd
import re





class twitter_credentials():
    # Variables that contains the user credentials to access Twitter API
    # This information is sensitive and will be deleted after the 20th June
    # Please create your own Twitter App if you plan to use future API applications
    CONSUMER_KEY = "yEKMKpNB81qQmm7i3c5LmjaUy"
    CONSUMER_SECRET = "l9QisbLYAHdUIufFPF6dkY1kyavZMJQ6nPVYpw05YEXRgAudbW"
    ACCESS_TOKEN = "1203071211397427200-YNnyt49cF9u9iLpWmeNY1DpIQl2RWD"
    ACCESS_TOKEN_SECRET = "8gQQVt8s43XStlPKMgFO9y1pQlGuIPJV85JLQZhAzoVBy"





''' Here I define my class that will use the Twitter client API to get the twitter user's timeline Tweets, friends list, home timeline tweets...'''
class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets







""" I pass these credentials to Tweepy’s OAuthHandler instance named ‘auth’,
 then using that instance I call the method set_access_token by passing the above-created access_key and, access_secret."""
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET) #oAuth handler class method
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET) #oAuth handler class method
        return auth






""" Class for streaming and processing live tweets. """
class TwitterStreamer():

    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authentication and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)








    """  This is a basic listener that just prints received tweets to stdout.  """
class TwitterListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        # certain twitter errors, like 420, create a cooldown time that grows exponentially the more you do it, we don't want these errors
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)







""" I clean the Tweet from hashtags, URLs.. then analyse the contents from tweets and categorise them, then send the to a pandas dataframe table"""
class TweetAnalyzer():

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df









if __name__ == '__main__':
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()

    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="Schwarzenegger", count=10)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

    print(df.head(10))

    #df.to_json(r'C:\Users\alans\OneDrive\Desktop\test\Twitter.json', orient='values')



    #Add these to the df table if needed
    # df['id'] = np.array([tweet.id for tweet in tweets])
    # df['len'] = np.array([len(tweet.text) for tweet in tweets])
    # df['date'] = np.array([tweet.created_at for tweet in tweets])