from bs4 import BeautifulSoup
import requests
import datetime
import time
import psycopg2

i = 5
prefectures = 'fukuoka'
from_date = datetime.date(2020, 2, 1)
to_date = datetime.date(2020, 2, 29)
url = f'https://connpass.com/search/?page={i}&q=&start_from={from_date.year}%2F{from_date.month}%2F{from_date.day}&start_to={to_date.year}%2F{to_date.month}%2F{to_date.day}&prefectures={prefectures}&selectItem={prefectures}'
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
events = soup.select('p.event_thumbnail img')
for event in events:
    print(event)
