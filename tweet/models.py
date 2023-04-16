from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=50, primary_key=True)


class Tweet(models.Model):
    id = models.BigIntegerField(primary_key=True)
    tweet = models.TextField(max_length=300)
    username = models.CharField(max_length=15)
    likes = models.IntegerField(default=0)
    retweets = models.IntegerField(default=0)
    quotes = models.IntegerField(default=0)
    source = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)


class Location(models.Model):
    location = models.CharField(max_length=50)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
