from datetime import date as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from scrayper import get_connpass
from db_helper import fetch_events
import json
import urllib


def scraype_and_insert_newevent_db(prefectures):
    from_date = dt.today()
    to_date = dt.today() + relativedelta(months=2)
    print(f"search from {from_date} to {to_date}")

    scrayped_events = get_connpass(prefectures, 1000, from_date, to_date)
    # print(scrayped_events)
    fetched_events = fetch_events(from_date, to_date, prefectures)
    # print(fetched_events)
    previours_event = set()
    current_event = set()
    for event in scrayped_events:
        current_event.add(event['event_name'])
    for event in fetched_events:
        previours_event.add(event[0])
    new_event_names = current_event - previours_event
    new_events = []
    # Log
    print(f"Fould new events:{new_event_names}")

    for new_event_name in new_event_names:
        for event in scrayped_events:
            if event['event_name'] == new_event_name:
                event['event_name'] = event['event_name'].replace("\'", "\'\'")
                new_events.append(event)

    if len(new_events) > 0:
        # TODO
        url = "https://conpass-notifier.herokuapp.com/cron"
        method = "POST"
        headers = {"Content-Type": "application/json"}
        # PythonオブジェクトをJSONに変換する
        json_data = json.dumps(new_events).encode("utf-8")
        # httpリクエストを準備してPOST
        request = urllib.request.Request(
            url, data=json_data, method=method, headers=headers)
        urllib.request.urlopen(request)


if __name__ == '__main__':
    scraype_and_insert_newevent_db("fukuoka")
    scraype_and_insert_newevent_db("online")
