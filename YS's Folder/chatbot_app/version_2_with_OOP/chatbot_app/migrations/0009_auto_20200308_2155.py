# Generated by Django 2.2.5 on 2020-03-08 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0008_auto_20200304_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='globalstatus',
            name='region',
        ),
        migrations.AddField(
            model_name='globalstatus',
            name='active',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]