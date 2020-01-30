from bs4 import BeautifulSoup
import requests
import datetime
import time
import psycopg2
from psycopg2.extras import DictCursor


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
            event = {}
            # replace ' to '' for postgresql.
            event['name'] = events_name[i].text.replace("\'", "\'\'")
            event['url'] = events_name[i]['href']
            event['date'] = events_year[i].text  + '/' + events_date[i].text
            event['img'] = events_img[i]['src']
            event['domain'] = 'connpass'
            events.append(event)
        time.sleep(0.8)
        previours_results = events_name
    return events


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
    prefectures = 'fukuoka'
    f_date = datetime.date(2020, 2, 1)
    t_date = datetime.date(2020, 2, 29)
    # events = get_connpass(prefectures, 2, f_date, t_date)
    # insertEvents(events, prefectures)
    fetch_events(f_date,t_date,prefectures)
