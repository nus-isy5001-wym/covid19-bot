# Generated by Django 2.2.10 on 2020-04-27 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0026_auto_20200427_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdiagnosis',
            name='check_in',
            field=models.BooleanField(default=False),
        ),
    ]
