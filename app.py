from flask import *
import requests
import datetime
import psycopg2
from bs4 import BeautifulStoneSoup
import scrayper
import lineApiTools
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


# CHANNEL_ACCESS_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']
CHANNEL_ACCESS_TOKEN = "aum5WMRALWyRx7EeFGQpqMIAKMRDxqtuyiQ6o5shAw1TsD6DDFElPxq4eJSoEAFvCWYLpZFljQNsojWI11hflZRGI1E54paRgrXp4om20XptO6151PKORWRjRWaAlurG/gQS6o6UA9mGRNqm3Pm9NwdB04t89/1O/w1cDnyilFU="
# CHANNEL_SECRET=os.environ['LINE_CHANNEL_SECRET']
CHANNEL_SECRET = "2b5ca5fb70f2a66347a0e059a7e05acf"
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
app = Flask(__name__)


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
    if event.message.text == "日時から探したい":
        message = lineApiTools.ask_fromdate()
        line_bot_api.reply_message(event.reply_token, message)


@handler.add(PostbackEvent)
def handle_postback(event):
    user_id=event.source.user_id
    cookie = event.postback.data.split(':')
    if cookie[0] == "from_date_message":
        from_date = datetime.date.fromisoformat(event.postback.params['date'])
        message = lineApiTools.ask_todate(from_date)
        line_bot_api.reply_message(event.reply_token, message)

    elif cookie[0] == "to_date_message":
        print(cookie[1])
        from_date = datetime.date.fromisoformat(cookie[1])
        to_date = datetime.date.fromisoformat(event.postback.params['date'])
        
        events = scrayper.fetch_events(from_date,to_date,'fukuoka')
        
        carousel = lineApiTools.gen_events_carousel(events)

        line_bot_api.push_message(user_id,TextSendMessage(text="検索中..."))
        for message in carousel:
            line_bot_api.push_message(
                to=user_id,messages=message
            )


@handler.add(FollowEvent)
def handle_follow(event):
    userID = event.source.user_id

    display_name = line_bot_api.get_profile(userID).display_name
    scrayper.insert_user_profile(userID, display_name)


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    scrayper.delete_user_profile(event.source.user_id)

# @handler.add("/cron/",methods=['POST'])
# def cron_handler():
#     pass

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
