from django.shortcuts import render
from django.http import JsonResponse
from tweet.models import Tweet, City

def get_tweets_of_city(request, city):
    tweets = Tweet.objects.filter(city__name=city)
    print(tweets[0].problem_type)
    problem_type = request.GET.get('problem_type', None)
    # print(problem_type)
    if problem_type is not None:
        tweets = tweets.filter(problem_type=problem_type)
    response = []
    for tweet in tweets:
        response.append({
            "id": tweet.id,
            "tweet": tweet.tweet,
            "username": tweet.username,
            "likes": tweet.likes,
            "retweets": tweet.retweets,
            "quotes": tweet.quotes,
            "source": tweet.source,
            "problem_type": tweet.problem_type
        })

    return JsonResponse({"tweets": response})

def get_names_of_city(request):
    cities = City.objects.all()
    cities = [city.name for city in cities]
    return JsonResponse({"cities": cities})
