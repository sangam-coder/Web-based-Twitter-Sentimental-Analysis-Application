

import pandas as pd

import streamlit as st
import tweepy
from PIL import Image
from textblob import TextBlob
import plotly.express as px

#Calculating Percentage

def percentage(part, whole):
    temp = 100 * float(part) / float(whole)
    return format(temp, '.2f')

# clean tweets

def cleantwt(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT[\s]+', '', text)
    text = re.sub(r'https:?\/\/\S+', '', text)

    return text

#Title For Web Based Application

st.title('*Twitter Sentiments Analysis*')
st.subheader("*Sentiments Analysis of tweets using Tweepy and TextBlob*")

# Import Image

image = Image.open('C:/Users/CODER/Downloads/R-project-sentiment-analysis.jpg')
st.image(image, caption='Sentiments', use_column_width=True)

# Twitter API Credentials

consumerKey = ''
consumerSecret = ''
Key = ''
Secret = ''

# Authenticating

a = tweepy.OAuthHandler(consumerKey, consumerSecret)
a.set_access_token(Key, Secret)
api = tweepy.API(a)

# input for tweet to be searched

SearchTweets = st.sidebar.text_input('Enter the keyword/hastag to search about','Donald')
NoOfTweets = st.sidebar.slider('Number of tweets',10,10000,150)

# Getting Tweets With The Help Of Tweepy

Tweets = tweepy.Cursor(api.search, q=SearchTweets, lang="en").items(NoOfTweets)

# creating some sentiments variable
polarity = 0
positive = 0
wpositive = 0
spositive = 0
negative = 0
wnegative = 0
snegative = 0
neutral = 0


# Clean Tweets By calling CleanTweet Function

Tweets = [cleantwt(tweet.text) for tweet in Tweets]

# Sentiments Statistics 

for tweet in Tweets:
           
    analysis = TextBlob(tweet)

    polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

    if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
    elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
    elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
    elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
    elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
    elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
    elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1

# Calculating Percentage By Calling Percentage function

positive = percentage(positive, NoOfTweets)
wpositive = percentage(wpositive, NoOfTweets)
spositive = percentage(spositive, NoOfTweets)
negative = percentage(negative, NoOfTweets)
wnegative = percentage(wnegative, NoOfTweets)
snegative = percentage(snegative, NoOfTweets)
neutral = percentage(neutral, NoOfTweets)

#putting up Data Together

data = {'Sentiment':['Positive','Neutral','Negative','Weaklypositive','StronglyPositive','WeaklyNegative','StronglyNegative'],
        'Result':[positive,wpositive,spositive,negative,wnegative,snegative,neutral]
        }
 
# Create DataFrame using Pandas
df = pd.DataFrame(data)


# Checking Sentiments With The Help Of TextBlob

sentiment_objects = [TextBlob(tweet) for tweet in Tweets]
sentiment_objects[0].polarity, sentiment_objects[0]

sentiment_values = [[str(tweet), tweet.sentiment.polarity] for tweet in sentiment_objects]
sentiment_values[0]


# creating DataFrame using Pandas

sentiment_df = pd.DataFrame(sentiment_values, columns=["tweet", "polarity"])
st.subheader("Tweets: ")
st.dataframe(sentiment_df,width=1080)


# Printing Statistics


st.subheader("How people are reacting on " + SearchTweets + " by analyzing " + str(NoOfTweets) + " tweets.")
fig = px.pie(df, values='Result', names='Sentiment', title=" ")
st.plotly_chart(fig)
st.subheader("""Detailed Report: """)
st.table(df)