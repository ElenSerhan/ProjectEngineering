# 16/03/2020
# Alan Serhan
# g00349187@gmit.ie
# https://github.com/ElenSerhan/ProjectEngineering/
"""
This example uses matplotlib to plot a graph of the analysis percentages.
"""

from textblob import TextBlob
import sys, tweepy
import matplotlib.pyplot as plt

def percentage(part, whole):
	return 100 * float(part)/float(whole)

# Declaring my keys and token
consumerKey = "yEKMKpNB81qQmm7i3c5LmjaUy"
consumerSecret = "l9QisbLYAHdUIufFPF6dkY1kyavZMJQ6nPVYpw05YEXRgAudbW"
accessToken = "1203071211397427200-YNnyt49cF9u9iLpWmeNY1DpIQl2RWD"
accessTokenSecret = "8gQQVt8s43XStlPKMgFO9y1pQlGuIPJV85JLQZhAzoVBy"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

searchTerm = input("Enter the twitter ID to search about: ")
noOfSearchTerms = int(input("Enter how many tweets to analyze: "))

tweets = tweepy.Cursor(api.user_timeline, id=searchTerm).items(noOfSearchTerms)

positive = 0
negative = 0
neutral = 0
polarity = 0

#function for analysing the tweet in textblob
for tweet in tweets:
    analysis = TextBlob(tweet.text)
    polarity += analysis.sentiment.polarity

    '''I Add a value to the variable and assign the result to that variable.'''
    if(analysis.sentiment.polarity == 0):
        neutral += 1
    elif(analysis.sentiment.polarity < 0.00):
        negative += 1
    elif(analysis.sentiment.polarity > 0.00):
        positive += 1

''' I assign the variable its sentiment depending on what the percentage is'''
positive = percentage(positive, noOfSearchTerms)
negative = percentage(negative, noOfSearchTerms)
neutral = percentage(neutral, noOfSearchTerms)
polarity = percentage(polarity, noOfSearchTerms)

''' chart format splitting my three sentiments'''
positive = format(positive, '.2f')
negative = format(negative, '.2f')
neutral = format(neutral, '.2f')

print("What we think user " + searchTerm + " is like by analysing " + str(noOfSearchTerms) + " Tweets.")

if (polarity == 0):
    print("Neutral")
elif (polarity < 0.00):
    print("Negative")
elif (polarity < 0.00):
    print("Positive")

labels = ['Positive [' + str(positive)+'%]', 'Negative [' + str(negative)+'%]', 'Neutral [' + str(neutral)+'%]']
sizes =[positive, negative, neutral]
colors = ['yellowgreen', 'red', 'gold']
patches, text = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title("What we think user " + searchTerm + " is like by analysing " + str(noOfSearchTerms) + " Tweets.")
plt.axis('equal')
plt.tight_layout()
plt.show()
plt.pie