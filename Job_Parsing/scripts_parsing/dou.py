# from selenium import webdriver  
 
# chrome_options = webdriver.ChromeOptions()  
# chrome_options.add_argument("--headless")
 
# driver = webdriver.Chrome(chrome_options=chrome_options)  
# driver.get("https://1xmavemv.com/ru/live/Handball/")


import requests	
from bs4 import BeautifulSoup 
import codecs


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
session = requests.Session()


jobs = []

def get_html(url):
    req = session.get(url, headers=headers)
    return req.text


def get_data(html):
		soup = BeautifulSoup(html, 'lxml')
		div_list = soup.find_all('div', attrs = {'class':'vacancy'})
		for div in div_list:
			title = div.find('div', class_='title').find('a').text
			href = div.find('div', class_='title').find('a').get('href')	
			short = div.find('div', class_='sh-info').text.strip()
			try:
				company = div.find('div', class_='title').find_all('a')[-1].text
			except:
				company = 'No name'
			jobs.append({'href':str(href), 'title':title, 'descript':short, 'company':company})


def main():
	base_url ='https://jobs.dou.ua/vacancies/?city=Киев&category=Python'

	get_data(get_html(base_url))



if __name__ == '__main__':
    main()