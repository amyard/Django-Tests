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





##############################################################################################
###################################        RABOTA         ####################################
##############################################################################################


def rabota(job, city, site, number_id):

	ua = UserAgent()
	headers = {'User-Agent':str(ua.chrome),
			  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
	session = requests.Session()

	urls = []
	jobs = []


	def get_main_info(job, city, site, number_id):
		if len(job.split(' ')) > 1:
			job = job.replace(' ', '+')
			city = number_id
			base_url = f'https://rabota.ua/jobsearch/vacancy_list?regionId={city}&keyWords={job}'
			pages = base_url+'&pg='
		else:
			job = job
			city = city.lower()
			base_url = f'https://rabota.ua/zapros/{job}/{city}'
			pages = base_url+'/pg'
		return city, job, base_url, pages


	def get_html(url):
	    req = session.get(url, headers=headers)
	    return req.text


	# дабы узнать количество страниц, спарсим количество вакансий, разделим на 15 и округлим
	def get_total_vacations(html):
		soup = BeautifulSoup(html, 'html.parser')
		total = soup.find('span', class_= 'fd-fat-merchant').text
		print(f'We have {int(np.ceil(int(total)/20))} pages ({int(total)}  vacancies).')
		return(np.ceil(int(total)/20))


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
				jobs.append({'url':domain+str(url), 'title':title, 'descript':short, 'company':company})	



	
	domain = 'https://rabota.ua'

	# получим значения
	city, job, base_url, pages = get_main_info(job, city, site, number_id)

	# проверяем правильность запроса
	req = session.get(base_url, headers=headers)
	if req.status_code == 200:
		total_pages = get_total_vacations(get_html(base_url))

		# парсим
		for i in range(1, int(total_pages)+1):
			# print('Loading {}%'.format(round((int(i)/int(total_pages))*100)))
			url = pages+str(i)
			print(url)
			get_data(get_html(url), domain)

	elif req.status_code != 200:
		print('Wrong data')
	return(jobs)



##############################################################################################
#################################        MAIN SCRIPT         #################################
##############################################################################################



job = 'python'
city = 'киев'
site = 0
number_id = 1

def main(job, city, site, number_id):

	if site == 0:
		# RABOTA.UA
		print('RABOTA')
		data = rabota(job, city, site, number_id)
		print(data)

		
	else:
		# WORK.UA
		print('WORK')

main(job, city, site, number_id)