#15/11/2019
#Alan Serhan
#g00349187@gmit.ie

import tweepy

# declaring my keys and token
consumer_key = "yEKMKpNB81qQmm7i3c5LmjaUy"
consumer_secret = "l9QisbLYAHdUIufFPF6dkY1kyavZMJQ6nPVYpw05YEXRgAudbW"
access_token = "1203071211397427200-YNnyt49cF9u9iLpWmeNY1DpIQl2RWD"
access_token_secret = "8gQQVt8s43XStlPKMgFO9y1pQlGuIPJV85JLQZhAzoVBy"

# Creating the authentication object
authentication = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting my access tokens and secret
authentication.set_access_token(access_token, access_token_secret)

# Creating the API object while passing in auth information
api = tweepy.API(authentication)
# Using the API object to get tweets from twitter's search query, and storing it in a variable called search
search = api.search("search_query")
# public_tweets = api.home_timeline()

# foreach through all tweets pulled
for items in search:
    # print text stored in items object
    print(items.text) 
