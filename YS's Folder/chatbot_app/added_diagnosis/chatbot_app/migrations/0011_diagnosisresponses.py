# Generated by Django 2.2.10 on 2020-04-07 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0010_hospitallist'),
    ]

    operations = [
        migrations.CreateModel(
            name='diagnosisResponses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(max_length=100)),
            ],
        ),
    ]
