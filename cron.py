from bs4 import BeautifulSoup
import requests
from datetime import date as dt
import psycopg2
from psycopg2.extras import DictCursor

def get_connpass(prefectures, page, from_date, to_date):
    events = list()
    page += 1
    previours_results = False
    for i in range(1, page):
        url = f'https://connpass.com/search/?page={i}&q=&start_from={from_date.year}%2F{from_date.month}%2F{from_date.day}&start_to={to_date.year}%2F{to_date.month}%2F{to_date.day}&prefectures={prefectures}&selectItem={prefectures}'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        events_name = soup.select('a.url.summary')
        events_date = soup.select('p.date')
        events_year = soup.select('p.year')
        events_img = soup.select('p.event_thumbnail img')
        if previours_results == events_name:
            return events
        # check to do rooping.
        for i in range(len(events_name)):

            # replace ' to '' for postgresql.
            event['name'] = events_name[i].text.replace("\'", "\'\'")
            event['url'] = events_name[i]['href']
            event['date'] = events_year[i].text + '/' + events_date[i].text
            event['img'] = events_img[i]['src']
            event['domain'] = 'connpass'
            events.append(event)
        time.sleep(0.5)
        previours_results = events_name
    return events

from_date = dt.today()
to_date = dt.today().

