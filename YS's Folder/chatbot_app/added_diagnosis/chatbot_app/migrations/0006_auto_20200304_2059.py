# Generated by Django 2.2.5 on 2020-03-04 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0005_auto_20200304_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mohheadlines',
            name='news_date',
            field=models.DateField(null=True),
        ),
    ]
