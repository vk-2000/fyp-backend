# Generated by Django 4.1.4 on 2023-06-18 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0004_alter_tweet_problem_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='media',
            field=models.CharField(default=None, max_length=50, null=True),
        ),
    ]