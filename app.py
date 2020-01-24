import flask
import requests
from bs4 import BeautifulStoneSoup
import scrayper
import line

app = flask(__name__)

@app.route('/')
def index():
	return '元気に動作中'

@app.route('/callback')
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
    if event.reply_token == "00000000000000000000000000000000":
        return

	if evnet.message.text == 'ふくおか':
		f_date = datetime.date(2020,1,1)
		t_date = datetime.date(2020, 1, 31)
		result = scrayper.get_connpass('fukuoka', 1, f_datem, t_date)
		line_bot_api.reply_message(
			event.reply_token, handle_message=result
		)
		


	