import requests	
from bs4 import BeautifulSoup 
import codecs
import numpy as np


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
session = requests.Session()


urls = []
jobs = []

def get_html(url):
    req = session.get(url, headers=headers)
    return req.text


# дабы узнать количество страниц, спарсим количество вакансий, разделим на 15 и округлим
def get_total_vacations(html):
	soup = BeautifulSoup(html, 'html.parser')
	total = soup.find('span', class_= 'fd-fat-merchant').text
	return(np.ceil(int(total)/20))


def get_data(html, domain):
		soup = BeautifulSoup(html, 'lxml')
		div_list = soup.find_all('article', class_='f-vacancylist-vacancyblock')
		for div in div_list:
			title = div.find('h3').text.strip()
			href = div.find('h3').find('a').get('href')	
			short = div.find('p', class_='fd-craftsmen').text.strip()
			try:
				company = div.p.text.strip()
			except:
				company = 'No name'
			jobs.append({'href':domain+str(href), 'title':title, 'descript':short, 'company':company})
			print(title)
		print('\n')	


def main():
	base_url ='https://rabota.ua/zapros/python/киев'
	pages = 'https://rabota.ua/zapros/python/киев/pg'
	domain = 'https://rabota.ua'
	
	total_pages = get_total_vacations(get_html(base_url))

	# парсим
	for i in range(1, int(total_pages)+1):
		url = pages+str(i)
		get_data(get_html(url), domain)



if __name__ == '__main__':
    main()