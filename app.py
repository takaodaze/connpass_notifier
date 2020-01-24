import requests
from bs4 import BeautifulSoup
 
r = requests.get("https://connpass.com/calendar/fukuoka/")
 
soup = BeautifulSoup(r.content, "html.parser")
 
# ニュース一覧を抽出
event_list = soup.select('a.Help')
for event in event_list:
	print(event.gw)
