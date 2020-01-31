from bs4 import BeautifulSoup
import requests
from datetime import date as dt
import time
import urllib
import json
import psycopg2
from psycopg2.extras import DictCursor
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


def insertEvent(event, prefectures):
    conn = connecter()
    sql = []
    sql.append(f'''
        INSERT INTO events VALUES
        ('{event["name"]}','{event["date"]}','{event["img"]}','{prefectures}','{event["domain"]}')
    ''')
    query(conn, sql)


def insertEvents(events, prefectures):
    conn = connecter()
    sql = []
    for event in events:
        sql.append(f'''
            INSERT INTO events VALUES
            ('{event["event_name"]}','{event["event_date"]}','{event["event_url"]}','{event["img_url"]}','{prefectures}','{event["domain"]}')
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
            event = {}
            # replace ' to '' for postgresql.
            event['event_name'] = events_name[i].text.replace("\'", "\'\'")
            event['event_url'] = events_name[i]['href']
            event['event_date'] = events_year[i].text  + '/' + events_date[i].text
            event['img_url'] = events_img[i]['src']
            event['domain'] = 'connpass'
            events.append(event)
        time.sleep(0.8)
        previours_results = events_name
    return events

#Dict
def fetch_events(from_date,to_date,prefectures):
    f_date_str = from_date.strftime("%Y/%m/%d")
    t_date_str = to_date.strftime("%Y/%m/%d")
    sql = f'''
        SELECT event_name,img_url,event_url,event_date
        FROM events
        WHERE event_date BETWEEN '{f_date_str}' AND '{t_date_str}'
        ORDER BY event_date ASC
    '''
    conn = connecter()
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(sql)
        events_dict = cur.fetchall()
    #events_dict is type:List
    return events_dict

def download_connpass():
    get_connpass = list()

def select_all_id():
    sql = f'SELECT DISTINCT user_id FROM users'
    conn = connecter()
    with conn.cursor() as cur:
        cur.execute(sql)
        all_id = cur.fetchall()
    return all_id


def insert_user_profile(userid,display_name):
    sql = f"INSERT INTO users VALUES('{userid}','{display_name}')"
    conn = connecter()
    with conn.cursor() as cur:
        cur.execute(sql)

def delete_user_profile(userid):
    sql = f"DELETE FROM users WHERE user_id = '{userid}'"
    conn = connecter()
    with conn.cursor() as cur:
        cur.execute(sql)



if __name__ == "__main__":
    prefectures = "fukuoka"
    from_date = dt.today()
    to_date = dt.today() + relativedelta(months=1)
    print(f"search from {from_date} to {to_date}")

    scrayped_events = get_connpass(prefectures, 1000, from_date, to_date)
    # print(scrayped_events)
    fetched_events = fetch_events(from_date,to_date,prefectures)
    # print(fetched_events)
    print(fetched_events[0]['event_name'])
    previours_event = set()
    current_event = set()
    for event in scrayped_events:
        current_event.add(event['event_name'])
    for event in fetched_events:
        previours_event.add(event[0])
    new_event_names = current_event-previours_event
    new_events = []

    for new_event_name in new_event_names:
        for event in scrayped_events:
            if event['event_name']==new_event_name:
                new_events.append(event)
    
    if len(new_events) > 0:
        url = "http://f95f01a9.ngrok.io/cron"
        method = "POST"
        headers = {"Content-Type": "application/json"}
        # PythonオブジェクトをJSONに変換する
        json_data = json.dumps(new_events).encode("utf-8")
        # httpリクエストを準備してPOST
        request = urllib.request.Request(
            url, data=json_data, method=method, headers=headers)
        urllib.request.urlopen(request)
