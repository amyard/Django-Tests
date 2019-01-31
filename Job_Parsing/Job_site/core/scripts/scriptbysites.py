import requests	
from bs4 import BeautifulSoup 
import codecs
import numpy as np
from fake_useragent import UserAgent
import sys
import re





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
			city = city
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

				try:
					date = ''.join(div.find('div', class_='f-vacancylist-bottomblock').find('p').text.strip().split(','))
					date =  'Сегодня' if re.search('час', date)  else date 
				except:
					date = 'Сегодня'
				jobs.append({'url':domain+str(url), 'title':title, 'descript':short, 'company':company, 'date':date})	



	
	domain = 'https://rabota.ua'

	# получим значения
	city, job, base_url, pages = get_main_info(job, city, site, number_id)

	# проверяем правильность запроса
	req = session.get(base_url, headers=headers)
	if req.status_code == 200:
		total_pages = get_total_vacations(get_html(base_url))

		# парсим
		for i in range(1, int(total_pages)+1):
			url = pages+str(i)
			get_data(get_html(url), domain)

	elif req.status_code != 200:
		print('Wrong data')
	return(jobs)