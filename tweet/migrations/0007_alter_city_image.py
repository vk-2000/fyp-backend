# Generated by Django 4.1.4 on 2023-06-18 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0006_city_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='image',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
    ]
