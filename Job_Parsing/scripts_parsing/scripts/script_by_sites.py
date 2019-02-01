import requests	
from bs4 import BeautifulSoup 
import codecs
import numpy as np
from fake_useragent import UserAgent
import sys
import re


job = 'junior qa'
city = 'киев'
site = 0
number_id = 1



##############################################################################################
###################################        RABOTA         ####################################
##############################################################################################


def rabota(job, city, site, number_id):

	ua = UserAgent()
	headers = {'User-Agent':str(ua.chrome),
			  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
	session = requests.Session()


	jobs = []


	def get_html(url):
	    req = session.get(url, headers=headers)
	    return req.text


	# дабы узнать количество страниц, спарсим количество вакансий, разделим на 15 и округлим
	def get_total_vacations(html):
		soup = BeautifulSoup(html, 'lxml')
		total = soup.find('span', class_= 'fd-fat-merchant').text
		return(np.ceil(int(total)/20), total)


	# дабы узнать количество страниц
	def get_count(html):
		soup = BeautifulSoup(html, 'lxml')
		total = soup.find('span', class_= 'fd-fat-merchant').text
		return total


	def get_data(html, domain):
			soup = BeautifulSoup(html, 'lxml')
			div_list = soup.find_all('article', class_='f-vacancylist-vacancyblock')
			for div in div_list:
				title = div.find('h3').text.strip()
				url = div.find('h3').find('a').get('href')	
				short = div.find('p', class_='fd-craftsmen').text.strip()
				try:
					company = div.p.text.strip()
				except:
					company = 'No name'

				try:
					date = ''.join(div.find('div', class_='f-vacancylist-bottomblock').find('p').text.strip().split(','))
					date =  'Сегодня' if re.search('час', date)  else date 
				except:
					date = 'Сегодня'
				jobs.append({'url':domain+str(url), 'title':title, 'descript':short, 'company':company, 'date':date})	



	url1 = 'https://rabota.ua/zapros/machine-learning-developer/киев'                                                                
	url2 = 'https://rabota.ua/zapros/machine-learning-developer/киев'                                                                
	url3 = 'https://rabota.ua/jobsearch/vacancy_list?regionId=1&keyWords=python'                                 
	url4 = 'https://rabota.ua/jobsearch/vacancy_list?regionId=1&keyWords=machine+learning+developer' 

	
	domain = 'https://rabota.ua'

	job = 'machine learning developer'

	job1 = job.replace(' ', '-') if len(job.split(' ')) > 1 else job
	job2 = job.replace(' ', '-')
	job3 = job.replace(' ', '+')
	# найдем лучший url
	urls = [f'https://rabota.ua/zapros/{job1}/{city}', f'https://rabota.ua/zapros/{job2}/{city}', 
			f'https://rabota.ua/jobsearch/vacancy_list?regionId={number_id}&keyWords={job1}',
			f'https://rabota.ua/jobsearch/vacancy_list?regionId={number_id}&keyWords={job3}']

	print(get_count(get_html(url3)))

	# ccc = [ get_count(get_html(url)) for url in urls ]
	# print(ccc)

	# job = 'junior-qa-automation-engineer'
	# city = 'киев'
	# site = 0
	# number_id = 1

	# base_url = f'https://rabota.ua/zapros/{job}/{city}'
	# # print(url)
	# # print(get_count(get_html(url)))

	# total_pages, total = get_total_vacations(get_html(base_url))
	# print(total)

			# base_url = f'https://rabota.ua/jobsearch/vacancy_list?regionId={city}&keyWords={job}'
			# base_url = f'https://rabota.ua/zapros/{job}/{city}'

	# проверяем правильность запроса
	# req = session.get(base_url, headers=headers)
	# if req.status_code == 200:
	# 	pages = base_url+'&pg=' if re.findall('vacancy_list', base_url) else base_url+'/pg'
	# 	total_pages, total = get_total_vacations(get_html(base_url))

	# 	# парсим
	# 	for i in range(1, int(total_pages)+1):
	# 		url = pages+str(i)
	# 		get_data(get_html(url), domain)

	# elif req.status_code != 200:
	# 	total = -1
	# 	jobs = None
	# 	return total, jobs

	# # return(jobs)
	# return total, jobs


rabota(job, city, site, number_id)