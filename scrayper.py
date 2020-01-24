from bs4 import BeautifulSoup
import requests
import datetime
import time

def get_connpass(prefectures, page, from_date, to_date):
	result_texts=[]
	page += 1
	previours_results = False
	for i in range(1,page):
		url = f'https://connpass.com/search/?page={i}&q=&start_from={from_date.year}%2F{from_date.month}%2F{from_date.day}&start_to={to_date.year}%2F{to_date.month}%2F{to_date.day}&prefectures={prefectures}&selectItem={prefectures}'
		r = requests.get(url)
		soup = BeautifulSoup(r.content, "html.parser")
		results = soup.select('a.url.summary')
		if previours_results == results and i!=1:
			return result_texts
		for event in results:
			result_texts.append(event.text)
		time.sleep(0.8)
		previours_results = results
	return result_texts
	

if __name__ == "__main__":
	f_date = datetime.date(2020,1,1)
	t_date = datetime.date(2020, 1, 31)
	result_texts = get_connpass('fukuoka', 40, f_date, t_date)
	for event in result_texts:
		print(event)

