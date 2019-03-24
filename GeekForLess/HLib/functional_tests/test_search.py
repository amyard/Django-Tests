from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest



class IndexTestCase(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.get('http://localhost:8000')
		self.browser.implicitly_wait(2)

	def tearDown(self):
		self.browser.quit()



	def test_search(self):
		# Search form real data
		search_box = self.browser.find_element_by_class_name('search-form')
		search_box.send_keys('Title')
		self.browser.find_elements_by_xpath("//*[contains(text(), 'Search')]")[0].click()
		self.browser.implicitly_wait(2)
		result = self.browser.find_element_by_tag_name('h3').text
		self.assertEqual(result, "Founded information (14):")
		print('Correct Data in Search Form')


		# Search form - wrong data
		search_box = self.browser.find_element_by_class_name('search-form')
		search_box.clear()
		search_box.send_keys('Yo-ho-ho')
		search_box.send_keys(Keys.ENTER)
		self.browser.implicitly_wait(2)
		result = self.browser.find_element_by_tag_name('h3').text
		self.assertEqual(result, "Sorry, we could not find anything.")
		print('Incorrect Data in Search Form')

		
		
if __name__ == '__main__':
	unittest.main(warnings='ignore')