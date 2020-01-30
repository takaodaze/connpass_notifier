from bs4 import BeautifulSoup
import requests
from datetime import date as dt
from datetime import timedelta
import psycopg2
from psycopg2.extras import DictCursor
import time
from dateutil.relativedelta import relativedelta


def connecter():
    conn = psycopg2.connect('''
    dbname=dopdifgtl4n9t
    host=ec2-54-235-66-1.compute-1.amazonaws.com
    user=yfneaarqpbzsuq
    password=4580d3a0e77f82e7bb199f8698e407eec8409c9f183bf094eccc1c755cf974e4
    ''')
    conn.autocommit = True
    return conn


def query(connecter, sql):
    with connecter.cursor() as cur:
        for s in sql:
            cur.execute(s)

def insertEvents(events, prefectures):
    conn = connecter()
    sql = []
    for event in events:
        sql.append(f'''
            INSERT INTO events VALUES
            ('{event["name"]}','{event["date"]}','{event["url"]}','{event["img"]}','{prefectures}','{event["domain"]}')
        ''')
    query(conn, sql)

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
            event = {}
            event['name'] = events_name[i].text.replace("\'", "\'\'")
            event['url'] = events_name[i]['href']
            event['date'] = events_year[i].text + '/' + events_date[i].text
            event['img'] = events_img[i]['src']
            event['domain'] = 'connpass'
            events.append(event)
        time.sleep(0.8)
        previours_results = events_name
    return events

from_date = dt.today()
# to_date = dt.today()+timedelta(days=4)
to_date = dt.today() + relativedelta(months=3)
print(f"serch from {from_date} to {to_date}")
events=get_connpass('fukuoka',1000,from_date,to_date)
insertEvents(events,'fukuoka')


