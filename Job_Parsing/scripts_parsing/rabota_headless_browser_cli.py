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


if len(sys.argv)>3:
	city = sys.argv[-1].lower()
	job = ' '.join([ argv.lower() for argv in sys.argv[1:-1] ])
else:
	city = sys.argv[-1].lower()
	job = sys.argv[1].lower()


ua = UserAgent()
headers = {'User-Agent':str(ua.chrome),
		  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
session = requests.Session()

urls = []
jobs = []


def get_url(url):
	options = webdriver.ChromeOptions()
	# options.add_argument('--headless')
	# driver = webdriver.Chrome(chrome_options=options)
	driver = webdriver.Chrome()
	driver.get(url)
	driver.find_element(By.XPATH, '//input[@id="ctl00_content_vacSearch_Keyword"]').send_keys(job)
	driver.find_element(By.XPATH, '//input[@id="ctl00_content_vacSearch_CityPickerWork_inpCity"]').clear()
	driver.find_element(By.XPATH, '//input[@id="ctl00_content_vacSearch_CityPickerWork_inpCity"]').send_keys(city)
	time.sleep(1)
	driver.find_element(By.XPATH, '//a[@id="ctl00_content_vacSearch_lnkSearch"]').click()
	url = driver.current_url
	driver.quit()
	return url


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
			jobs.append({'url':domain+str(url), 'title':title, 'descript':short, 'company':company})
			print(title)
		print('\n')	


def main():
	domain = 'https://rabota.ua'

	# получил url нашей страници
	base_url = get_url(domain)
	print(base_url)

	# проверяем правильность запроса
	req = session.get(base_url, headers=headers)
	if req.status_code == 200:
		pages = base_url+'&pg=' if re.findall('vacancy_list', base_url) else base_url+'/pg'
		total_pages = get_total_vacations(get_html(base_url))
		print(f'We have {int(total_pages)} pages.')


		# парсим
		for i in range(1, int(total_pages)+1):
			print('Loading {}%'.format((int(i)/int(total_pages))*100))
			url = pages+str(i)
			get_data(get_html(url), domain)

	elif req.status_code != 200:
		print('Wrong data')
	



if __name__ == '__main__':
    main()