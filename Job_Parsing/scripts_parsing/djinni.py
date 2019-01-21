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
	total = soup.find('div', class_= 'page-header').find('small').text
	return(np.ceil(int(total)/15))


def get_data(html, domain):
		soup = BeautifulSoup(html, 'lxml')
		div_list = soup.find('ul', attrs = {'class':'list-jobs'}).find_all('li', class_='list-jobs__item')
		for div in div_list:
			title = div.find('a').text
			href = div.find('a').get('href')	
			short = div.p.text
			try:
				company = ' '.join(div.find('div',class_='list-jobs__details').text.strip().split(',')[1].split())
			except:
				company = 'No name'
			jobs.append({'href':domain+str(href), 'title':title, 'descript':short, 'company':company})


def main():
	base_url ='https://djinni.co/jobs/?primary_keyword=Python&location=Киев'
	domain = 'https://djinni.co/jobs'
	# second_page = 'https://djinni.co/jobs/?location=%D0%9A%D0%B8%D0%B5%D0%B2&page=2&primary_keyword=Python'

	total_pages = get_total_vacations(get_html(base_url))

	# на сайте если ввести page=1 сбрасывает все настройки поиска и открывает начальную страницу.
	# создадим список url для парсинга.
	urls.append(base_url)
	for i in range(2, int(total_pages)+1):
		urls.append(base_url + '&page=' + str(i))

	[ get_data(get_html(url), domain) for url in urls ]


if __name__ == '__main__':
    main()