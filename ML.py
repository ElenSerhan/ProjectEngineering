import tweepy

consumer_key = "xxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxx"
access_token = "xxxxxxxxxxxxxxx"
access_token_secret = "xxxxxxxxxxxxxx"

authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
authentication.set_access_token(access_token, access_token_secret)

api = tweepy.API(authentication)
search = api.search("search_query")

for items in search:
    print(items.text)
