# Generated by Django 2.2.5 on 2020-03-04 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0006_auto_20200304_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mohheadlines',
            name='news_link',
            field=models.URLField(unique=True),
        ),
    ]
