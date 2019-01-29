import requests	
from bs4 import BeautifulSoup 
import codecs
import numpy as np
from fake_useragent import UserAgent
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time


# def get_main_info():
# 	if len(sys.argv)>3:
# 		translate = {'все регионы': 0, 
# 					 'киев': 1,
# 					 'львов': 2,
# 					 'одесса': 3, 
# 					 'днепр': 4,
# 					 'винница': 5,
# 					 'донецк': 6,
# 					 'житомир': 7,
# 					 'запорожье': 9,
# 					 'ивано-франковск': 10,
# 					 'кропивницкий': 11,
# 					 'луганск': 13,				 
# 					 'луцк': 14,
# 					 'николаев': 15,
# 					 'полтава': 17,
# 					 'ровно': 18,
# 					 'сумы': 19,
# 					 'тернополь': 20,
# 					 'харьков': 21,
# 					 'херсон': 22,
# 					 'хмельницкий': 23,
# 					 'черкассы': 24,
# 					 'чернигов': 25,
# 					 'черновцы': 26,				 
# 					 'мариуполь': 27,
# 					 'ужгород': 28,
# 					 'симферополь': 29,
# 					 'кривой рог': 31,
# 					 'севастополь': 32}
# 		city = translate.get(sys.argv[-1].lower(),sys.argv[-1].lower())
# 		job = '+'.join([ argv.lower() for argv in sys.argv[1:-1] ])
# 		base_url = f'https://rabota.ua/jobsearch/vacancy_list?regionId={city}&keyWords={job}'
# 		pages = base_url+'&pg='
# 	else:
# 		city = sys.argv[-1].lower()
# 		job = sys.argv[1].lower()
# 		base_url = f'https://rabota.ua/zapros/{job}/{city}'
# 		pages = base_url+'/pg'
# 	return city, job, base_url, pages


# ua = UserAgent()
# headers = {'User-Agent':str(ua.chrome),
# 		  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
# session = requests.Session()

# urls = []
# jobs = []



# def get_html(url):
#     req = session.get(url, headers=headers)
#     return req.text


# # дабы узнать количество страниц, спарсим количество вакансий, разделим на 15 и округлим
# def get_total_vacations(html):
# 	soup = BeautifulSoup(html, 'html.parser')
# 	total = soup.find('span', class_= 'fd-fat-merchant').text
# 	print(f'We have {int(np.ceil(int(total)/20))} pages ({int(total)}  vacancies).')
# 	return(np.ceil(int(total)/20))


# def get_data(html, domain):
# 		soup = BeautifulSoup(html, 'lxml')
# 		div_list = soup.find_all('article', class_='f-vacancylist-vacancyblock')
# 		for div in div_list:
# 			title = div.find('h3').text.strip()
# 			url = div.find('h3').find('a').get('href')	
# 			short = div.find('p', class_='fd-craftsmen').text.strip()
# 			try:
# 				company = div.p.text.strip()
# 			except:
# 				company = 'No name'
# 			jobs.append({'url':domain+str(url), 'title':title, 'descript':short, 'company':company})
# 			print(title)
# 		print('\n')	


# def main():

# 	domain = 'https://rabota.ua'

# 	# получим значения
# 	city, job, base_url, pages = get_main_info()

# 	# проверяем правильность запроса
# 	req = session.get(base_url, headers=headers)
# 	if req.status_code == 200:
# 		total_pages = get_total_vacations(get_html(base_url))

# 		# парсим
# 		for i in range(1, int(total_pages)+1):
# 			print('Loading {}%'.format(round((int(i)/int(total_pages))*100)))
# 			url = pages+str(i)
# 			print(url)
# 			get_data(get_html(url), domain)

# 	elif req.status_code != 200:
# 		print('Wrong data')
	


# if __name__ == '__main__':
#     main()



if len(sys.argv)>3:
		translate = {'все регионы': 0, 
					 'киев': {1, 'kiev'},
					 'львов': 2,
					 'одесса': 3, 
					 'днепр': 4,
					 'винница': 5,
					 'донецк': 6,
					 'житомир': 7,
					 'запорожье': 9,
					 'ивано-франковск': 10,
					 'кропивницкий': 11,
					 'луганск': 13,				 
					 'луцк': 14,
					 'николаев': 15,
					 'полтава': 17,
					 'ровно': 18,
					 'сумы': 19,
					 'тернополь': 20,
					 'харьков': 21,
					 'херсон': 22,
					 'хмельницкий': 23,
					 'черкассы': 24,
					 'чернигов': 25,
					 'черновцы': 26,				 
					 'мариуполь': 27,
					 'ужгород': 28,
					 'симферополь': 29,
					 'кривой рог': 31,
					 'севастополь': 32}
city = translate.get(sys.argv[-1].lower(),sys.argv[-1].lower())
