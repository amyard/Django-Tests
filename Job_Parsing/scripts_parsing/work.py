import requests	
from bs4 import BeautifulSoup 
import codecs


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
session = requests.Session()


urls = []
jobs = []

def get_html(url):
    req = session.get(url, headers=headers)
    return req.text


def get_paggination_links(html, base_url, domain):
	urls.append(base_url)
	soup = BeautifulSoup(html, 'html.parser')
	pagination = soup.find('ul', class_= 'pagination')
	if pagination:
		pages = pagination.find_all('li')
		[ urls.append(domain+str(page.a['href'])) for page in pages[2:-1] ]
	return urls


def get_data(html, domain):
		soup = BeautifulSoup(html, 'html.parser')
		div_list = soup.find_all('div', attrs = {'class':'job-link'})
		for div in div_list:
			title = div.find('h2').find('a').text
			href = div.find('h2').find('a').get('href')	
			short = div.p.text
			try:
				company = div.find('b').text
			except:
				company = 'No name'
			jobs.append({'href':domain+str(href), 'title':title, 'descript':short, 'company':company})


def main():
	base_url ='https://www.work.ua/jobs-kyiv-python/'
	domain = 'https://www.work.ua'

	# url в пагинации
	urls = get_paggination_links(get_html(base_url), base_url, domain)

	# парсим данные
	[ get_data(get_html(url), domain) for url in urls ]



if __name__ == '__main__':
    main()