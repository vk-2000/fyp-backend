from tweet.models import City
from snscrape.modules.twitter import TwitterSearchScraper
import pickle
import re
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm')


def pre_process(tweet_str):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    str1 = emoji_pattern.sub(r'', tweet_str)  # no emoji
    str1 = ' '.join(
        re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", str1).split())

    # print(str1)
    return str1


def classify_tweet(tweet):
    loaded_vectorizer = pickle.load(open("ml_model/vector.pickle", "rb"))
    naive_bayes = pickle.load(open("ml_model/model.pickle", "rb"))

    pre_processed_tweet = pre_process(tweet.content)
    df = pd.Series([pre_processed_tweet])

    trial1 = loaded_vectorizer.transform(df)
    predict = naive_bayes.predict(trial1)
    return predict == '1'


def extract_tweets_and_classify(city):
    tweets = []
    for i, tweet in enumerate(TwitterSearchScraper(f'near: {city}').get_items()):
        if i > 10:
            break
        tweets.append(tweet)

    classified_tweets = list(filter(classify_tweet, tweets))
    # print(classified_tweets)
    return classified_tweets


def extract_locations(tweet):
    doc = nlp(tweet.content)
    locations = [e.text
                 for e in doc.ents if e.label_ in ('FAC', 'LOC', 'EVENT', 'GPE', 'ORG')]
    return locations


def update_database():
    pass


def periodic():
    # extract tweets from every city (city table) and classify the tweets
    print("Periodic process started")
    cities = City.objects.values_list('name')
    for city in cities:
        tweets = extract_tweets_and_classify(city)
        for tweet in tweets:
            # for every tweet
            locations = extract_locations(tweet)
            print(tweet.content)
            print(locations)
            pass
