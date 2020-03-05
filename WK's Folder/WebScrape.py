import sys
import django
import os
os.environ.setdefault('DJANGO_SETTING_MODULE', 'ChatBot_Main.settings')
# setting can be found in wsgi.py folder in pycache
os.environ['DJANGO_SETTINGS_MODULE'] = 'ChatBot_Main.settings'
#os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from chatbot_app.models import globalStatus, globalLastUpdate, MOHHeadlines
import pandas as pd
from requests import get
from bs4 import BeautifulSoup
from datetime import datetime

#### FOR GLOBAL STATUS - FOR INFECTION STATUS INTENT ####

globalLastUpdate.objects.all().delete()

url = 'https://www.worldometers.info/coronavirus/'
html_soup = get(url)
html_soup = BeautifulSoup(html_soup.text, 'html.parser')
LastUpdatetext = html_soup.find(
    'div', class_='content-inner').find_all('div')[1].getText()

table_rows = html_soup.find(
    'table', attrs={'id': 'main_table_countries'}).find_all('tr')
res = []
for tr in table_rows[1:]:
    td = tr.find_all('td')
    row = []
    for i in td:
        val = i.text.strip().replace('+', '').replace(',', '').replace(' *','').lower() if i.text.strip() != "" else 0
        try:
            val = int(val)
        except:
            val = val
        row.append(val)
    res.append(row)
# globalStatus.objects.create(country = row[0], diagnosed = row[1], new_cases = row[2], death = row[3], new_death = row[4], discharged = row[5], critical = row[6], region = row[7])

col = ['country', 'diagnosed', 'new_cases', 'death',
    'new_death', 'discharged', 'critical', 'region']
pd_table = pd.DataFrame(res, columns=col)
global_dict = pd_table.to_dict('records')
model_instance = [globalStatus(country=i['country'], diagnosed=i['diagnosed'], new_cases=i['new_cases'], death=i['death'], new_death=i['new_death'], discharged=i['discharged'], critical=i['critical'], region=i['region']) for i in global_dict]


try:
    globalStatus.objects.bulk_create(model_instance)
    print('Update globalStatus complete!')
except:
    print('Error occurred. Either something went wrong or data already exist.')

try:
    globalLastUpdate.objects.create(last_update=LastUpdatetext)
    print('Update globalLastUpdate complete!')
except:
    print('Error occurred. Update globalLastUpdate unsuccessful.')


###############

class Webscrapper():

    def __init__(self):
        self.headline = None
        self.link = None

    def start(self):
        url = 'https://www.moh.gov.sg/covid-19'
        response = get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        a = soup.findAll('table')[2].findAll('tr')

        for i, news in enumerate(a[1:]):
            dict = {
                    'news_date' : datetime.strptime(news.findAll('td')[0].getText().replace('\xa0', ''), '%d %b %Y').date(),
                    'news_title' : news.findAll('td')[1].getText().replace('\xa0',''),
                    'news_link' : news.findAll('a', href=True)[0]['href']
                    }
            try:
                MOHHeadlines.objects.create(**dict) #use ** to add dict into models
                print(f'Title {i+1} updated successfully')
            except:
                print(f'Title {i+1} failed to update or data already exist')

ws = Webscrapper()
ws.start()
