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

@app.route('/callback',methods=['POST'])
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
    if event.message.text == "ふくおか":
        f_date = datetime.date(2020,2,1)
        t_date = datetime.date(2020, 2, 29)
        events = scrayper.fetch_events(f_date,t_date,'fukuoka')
        carousel = lineApiTools.gen_events_carousel(events)

        for message in carousel:
            line_bot_api.push_message(
                user_id,messages=message
            )
        

        
if __name__ == "__main__":
    app.run(debug=True,port=8080)
    
