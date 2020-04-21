# Generated by Django 2.2.5 on 2020-04-20 09:06

import chatbot_app.modules.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot_app', '0019_delete_graphplot'),
    ]

    operations = [
        migrations.CreateModel(
            name='graphPlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('plot', models.ImageField(storage=chatbot_app.modules.storage.OverwriteStorage(), upload_to='plots/')),
                ('datetime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]