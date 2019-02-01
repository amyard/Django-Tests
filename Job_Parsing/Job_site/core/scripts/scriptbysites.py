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
			# base_url = f'https://rabota.ua/jobsearch/vacancy_list?regionId={city}&keyWords={job}'
			# pages = base_url+'&pg='
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
		# return(np.ceil(int(total)/20))
		return(np.ceil(int(total)/20), total)


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
					date =  'Сегодня' if re.search('час', date) or re.search('мин', date)  else date 
				except:
					date = 'Сегодня'
				jobs.append({'url':domain+str(url), 'title':title, 'descript':short, 'company':company, 'date':date})	



	
	domain = 'https://rabota.ua'

	# получим значения
	city, job, base_url, pages = get_main_info(job, city, site, number_id)


	try:
		req = session.get(base_url, headers=headers)
		if req.status_code == 200:
			# total_pages = get_total_vacations(get_html(base_url))
			total_pages, total = get_total_vacations(get_html(base_url))

			# парсим
			for i in range(1, int(total_pages)+1):
				url = pages+str(i)
				get_data(get_html(url), domain)

			# return(jobs)
			return total, jobs	
		elif req.status_code != 200:
			total = -1
			jobs = None
			return total, jobs	
	except:

		base_url = f'https://rabota.ua/jobsearch/vacancy_list?regionId={number_id}&keyWords={job}'
		pages = base_url+'&pg='

		req = session.get(base_url, headers=headers)
		if req.status_code == 200:
			# total_pages = get_total_vacations(get_html(base_url))
			total_pages, total = get_total_vacations(get_html(base_url))

			# парсим
			for i in range(1, int(total_pages)+1):
				url = pages+str(i)
				get_data(get_html(url), domain)

			# return(jobs)
			return total, jobs	
		elif req.status_code != 200:
			total = -1
			jobs = None
			return total, jobs



##############################################################################################
###################################        Work         ####################################
##############################################################################################


def work(job, slug, site, number_id):

	ua = UserAgent()
	headers = {'User-Agent':str(ua.chrome),
			  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
	session = requests.Session()

	urls = []
	jobs = []



	def get_html(url):
	    req = session.get(url, headers=headers)
	    return req.text


	def get_total(html):
		soup = BeautifulSoup(html, 'lxml')
		try:
			pagination = soup.find('div', class_= 'card').find('div', class_= 'add-top').text.strip()
			total =  ''.join(re.findall(r'\d+',pagination))
			return(np.ceil(int(total)/14), total)
		except:
			return 0, 0


	def get_data(html, domain):
		soup = BeautifulSoup(html, 'lxml')
		div_list = soup.find_all('div', attrs = {'class':'job-link'})
		for div in div_list:
			title = div.find('h2').find('a').text
			href = div.find('h2').find('a').get('href')	
			short = div.p.text
			try:
				company = div.find('b').text
			except:
				company = 'No name'

			date = div.find_all('span')
			
			# Date Preprocessing
			asd = [ d.text  for d in date if re.search('год', d.text.strip()) \
												or re.search('Гаря', d.text.strip()) \
												or re.search('хвилин', d.text.strip()) \
												or re.search('Сьогод', d.text.strip()) \
												or re.search('Вчора', d.text.strip()) \
												or re.search('дні', d.text.strip()) \
												or re.search('тиж', d.text.strip())]
			for i in asd:
				date = i.replace(' · ', '')
				if re.search('1 тижд.', date):
					date = '1 неделю назад'
				elif re.search('год', date) or re.search('хвилин', date) or re.search('Гаря', date):
					date = 'Сегодня'
				elif re.search('Вчора', date):
					date = '1 день назад'
				elif re.search('5 дні', date) or re.search('6 дні', date) or re.search('7 дні', date):
					date = date.replace('днів тому', 'дней назад')

				date = date.replace('дні тому', 'дня назад')
				date = date.replace('тижд. тому', 'недели назад')

			jobs.append({'url':domain+str(href), 'title':title, 'descript':short, 'company':company, 'date': date})
	


	domain = 'https://www.work.ua'
	job = job.replace(' ', '+') if len(job.split(' ')) > 1 else job


	# для всей Украины слага нету
	if number_id == 0:
		base_url = f'https://www.work.ua/jobs-{job}/'
	else:
		base_url = f'https://www.work.ua/jobs-{slug}-{job}/'


	req = session.get(base_url, headers=headers)
	if req.status_code == 200:

		total_pages, total = get_total(get_html(base_url))
		# парсим
		for i in range(1, int(total_pages)+1):
			url = base_url+'?page='+str(i)
			get_data(get_html(url), domain)
		return total, jobs

	elif req.status_code != 200:
		total = -1
		jobs = None
		return total, jobs