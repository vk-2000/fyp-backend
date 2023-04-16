# Generated by Django 4.1.4 on 2023-04-16 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0002_tweet_problem_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='problem_type',
            field=models.CharField(choices=[('INF', 'Infrastructure'), ('PUB', 'Public safety'), ('SER', 'Services failure')], default=None, max_length=3),
        ),
    ]
