import requests	
from bs4 import BeautifulSoup 
import codecs
import numpy as np
from fake_useragent import UserAgent
import sys
import re


job = 'javascript'
slug = 'kyiv'
site = None
number_id = None

# job = 'account manager asd'



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

			jobs.append({'href':domain+str(href), 'title':title, 'descript':short, 'company':company, 'date': date})
	


	domain = 'https://www.work.ua'
	job = job.replace(' ', '+') if len(job.split(' ')) > 1 else job


	# для всей Украины слага нету
	if slug == 0:
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

work(job, slug, site, number_id)