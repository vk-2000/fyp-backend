from tweet.models import City, Tweet
from snscrape.modules.twitter import TwitterSearchScraper
import pickle
import re
import pandas as pd
from nltk.corpus import stopwords
import spacy
nlp = spacy.load('en_core_web_sm')


def is_spam(tweet):
    
    with open('ml_model/models_pkl/model_spam.pkl', 'rb') as f:
        model_spam = pickle.load(f)

    with open('ml_model/models_pkl/vectorizer_spam.pkl', 'rb') as f:
        vectorizer_spam = pickle.load(f)
    tweet = re.sub('[^a-zA-Z0-9\s]', '', tweet)
    tweet = tweet.lower()
    # nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    tweet = ' '.join([word for word in tweet.split() if word not in stop_words])
    X = vectorizer_spam.transform([tweet])
    y = model_spam.predict(X)
    if y == 1:
        return True
    else:
        return False

def classify_tweet(tweet):
    with open('ml_model/models_pkl/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('ml_model/models_pkl/vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    tweet = re.sub('[^a-zA-Z0-9\s]', '', tweet)
    tweet = tweet.lower()
    # nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    tweet = ' '.join([word for word in tweet.split() if word not in stop_words])
    X = vectorizer.transform([tweet])
    y = model.predict(X)
    return y[0]


def extract_tweets_and_classify(city):
    tweets = []
    for i, tweet in enumerate(TwitterSearchScraper(f'near: {city}').get_items()):
        if i > 300:
            break
        if not is_spam(tweet.content):
            tweets.append(tweet)
    
    for tweet in tweets:
        tweet.problem_type = classify_tweet(tweet.content)
    
    tweets = [tweet for tweet in tweets if tweet.problem_type != 'unproblematic']

    return tweets

    


# def extract_locations(tweet):
#     doc = nlp(tweet.content)
#     locations = [e.text
#                  for e in doc.ents if e.label_ in ('FAC', 'LOC', 'EVENT', 'GPE', 'ORG')]
#     return locations


def update_database():
    pass


def periodic():
    # extract tweets from every city (city table) and classify the tweets
    print("Periodic process started")
    cities = City.objects.all()
    for city in cities:
        tweets = extract_tweets_and_classify(city.name)
        for tweet in tweets:

            if Tweet.objects.filter(id=tweet.id).exists():
                continue
            
            Tweet.objects.create(
                id=tweet.id,
                tweet=tweet.content,
                username=tweet.username,
                likes=tweet.likeCount,
                retweets=tweet.retweetCount,
                quotes=tweet.quoteCount,
                source=tweet.source,
                city=city,
                problem_type=tweet.problem_type
            )
