import psycopg2
from psycopg2.extras import DictCursor
from datetime import date as dt
from datetime import timedelta

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
    now_date_str = dt.today().isoformat()
    for event in events:
        sql.append(f'''
            INSERT INTO events(
                event_name,event_date,event_url,
                img_url,prefectures,insert_date
            )
            VALUES
            ('{event["event_name"]}',
            '{event["event_date"]}',
            '{event["event_url"]}',
            '{event["img_url"]}',
            '{prefectures}',
            current_date)
        '''
                   )
    query(conn, sql)

def fetch_events(from_date, to_date, prefectures):
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
    # events_dict is type:List
    return events_dict

def fetch_thisweek_events():
    conn = connecter()
    delta = timedelta(days=7)
    to_date_str = (dt.today()+delta).isoformat()

    sql = f"""
    SELECT event_name,img_url,event_url,event_date
    FROM events
    WHERE event_date BETWEEN current_date AND '{to_date_str}'
    ORDER BY event_date DESC
    LIMIT 50
    """

    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(sql)
        events_dict = cur.fetchall()
    return events_dict

def fetch_recentlly_events(prefectures):
    conn = connecter()
    delta = timedelta(days=4)
    to_date_str = dt.today().isoformat()
    from_date_str = (dt.today()-delta).isoformat()
    sql = f"""
        SELECT event_name,img_url,event_url,event_date
        FROM events
        WHERE insert_date BETWEEN '{from_date_str}' AND current_date
        AND event_date >= current_date
        AND insert_date IS NOT NULL
        ORDER BY insert_date 
        LIMIT 50
    """
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(sql)
        events_dict = cur.fetchall()
    # events_dict is type:List
    return events_dict

def select_all_id():
    sql = f'SELECT DISTINCT user_id FROM users'
    conn = connecter()
    with conn.cursor() as cur:
        cur.execute(sql)
        all_id = cur.fetchall()
    return all_id

def insert_user_profile(userid, display_name):
    sql = f"INSERT INTO users VALUES('{userid}','{display_name}')"
    conn = connecter()
    with conn.cursor() as cur:
        cur.execute(sql)

def delete_user_profile(userid):
    sql = f"DELETE FROM users WHERE user_id = '{userid}'"
    conn = connecter()
    with conn.cursor() as cur:
        cur.execute(sql)

def delete_event(event_name):
    sql = f"DELETE FROM events WHERE event_name = '{event_name}'"
    conn = connecter()
    with conn.cursor() as cur:
        cur.execute(sql)
