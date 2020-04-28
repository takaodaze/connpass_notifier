import os
from flask import *
import requests
import datetime
import pprint
import psycopg2
from bs4 import BeautifulStoneSoup
import scrayper
import db_helper
import lineApiTools
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import time
from flex import Flex
import flask


CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET=os.environ['LINE_CHANNEL_SECRET']
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
app = Flask(__name__)

flex = Flex()

@app.route('/favicon.ico')
def favicon():
    return "OK.There is noting!"


@app.route('/')
def index():
    return '元気に動作中'


@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # https://developers.line.biz/console/channel/1653365219/basic/
    # LINEコンソールのwebhook URL のエラー回避用.
    user_id = event.source.user_id
    if event.reply_token == "00000000000000000000000000000000":
        return
    if event.message.text == "日時から探したい":
        message = flex.gen_from_datepicker()
        line_bot_api.reply_message(event.reply_token, message)
    elif event.message.text == "新着のイベントを教えて":
        flex_message = lineApiTools.gen_recentlly_event_flex_list('fukuoka')
        if len(flex_message)==0:
           line_bot_api.reply_message(
               event.reply_token, TextSendMessage("福岡の新着イベントは\n1件も見つからなかったよ...\nごめんね..."))
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif event.message.text == "今週のイベントを教えて":
        events = db_helper.fetch_thisweek_events()
        flex_message = lineApiTools.gen_events_flex_carousel_list(events=events)
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        start_message = flex.gen_start_flex()
        line_bot_api.reply_message(event.reply_token, start_message)
        

@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    cookie = event.postback.data.split(':')
    print(cookie)
    if cookie[0] == "from_date_message":
        from_date = datetime.date.fromisoformat(event.postback.params['date'])
        message = flex.gen_to_datepicker(from_date)
        line_bot_api.reply_message(event.reply_token, message)

    elif cookie[0] == "to_date_message":
        from_date = datetime.date.fromisoformat(cookie[1])
        to_date = datetime.date.fromisoformat(event.postback.params['date'])

        events = db_helper.fetch_events(from_date, to_date, 'fukuoka')
        carousel = lineApiTools.gen_events_flex_carousel_list(events)
        
        if 0 < len(carousel) <= 5:  
            line_bot_api.reply_message(event.reply_token, carousel)
        elif len(carousel)>5:
            line_bot_api.reply_message(event.reply_token,TextSendMessage("検索結果が多すぎたよ...\nもう少し期間を狭めてほしいな..."))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage("1件も見つからなかった...\nごめんね..."))

@handler.add(FollowEvent)
def handle_follow(event):
    userID = event.source.user_id

    display_name = line_bot_api.get_profile(userID).display_name

    db_helper.insert_user_profile(userID, display_name)
    flex_message = flex.gen_start_flex()
    line_bot_api.reply_message(event.reply_token, flex_message)

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    db_helper.delete_user_profile(event.source.user_id)

# TODO shold be logging!!!!
@app.route('/cron/<prefecture>/', methods=['POST'])
def cron_handler(prefecture):
    if request.headers['Content-Type'] != 'application/json':
        print(request.headers['Content-Type'])
        return flask.jsonify(res='error'), 400

    for event in request.json:
        event['event_date'] = datetime.date.fromisoformat(
            event['event_date'].replace('/', '-'))

    # message_list = lineApiTools.gen_events_flex_carousel_list(request.json)
    db_helper.insertEvents(request.json,prefecture) 

    return jsonify(res='ok')


if __name__ == "__main__":
    app.run(port=5000)