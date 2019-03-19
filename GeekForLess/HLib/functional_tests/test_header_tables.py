# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import unittest
# from django.urls import reverse



# class IndexTestCase(unittest.TestCase):

# 	def setUp(self):
# 		self.browser = webdriver.Firefox()
# 		self.browser.get('http://localhost:8000')
# 		self.browser.implicitly_wait(2)

# 	def tearDown(self):
# 		self.browser.quit()

	
# 	def test_header_all_tables(self):

# 		# All Books
# 		general_button = self.browser.find_elements_by_xpath("//a[contains(text(), 'General Information')]")[0]
# 		general_button.click()

# 		menuItem = self.browser.find_element_by_link_text('All books')
# 		menuItem.click()
# 		self.assertIn('http://localhost:8000', self.browser.current_url)
# 		header3 = self.browser.find_element_by_tag_name('h3').text
# 		self.assertIn('All books:', header3)
# 		self.browser.implicitly_wait(1)
# 		print('All Books worked.')




# 		# Books in library
# 		general_button = self.browser.find_elements_by_xpath("//a[contains(text(), 'General Information')]")[0]
# 		general_button.click()

# 		menuItem = self.browser.find_element_by_link_text('In library')
# 		menuItem.click()
# 		self.assertIn('http://localhost:8000/books-in-library', self.browser.current_url)
# 		header3 = self.browser.find_element_by_tag_name('h3').text
# 		self.assertIn('Books in library:', header3)
# 		self.browser.implicitly_wait(1)
# 		print('Books in library worked.')




# 		# Books on hands
# 		general_button = self.browser.find_elements_by_xpath("//a[contains(text(), 'General Information')]")[0]
# 		general_button.click()

# 		menuItem = self.browser.find_element_by_link_text('On hands')
# 		menuItem.click()
# 		self.assertIn('http://localhost:8000/books-on-hands', self.browser.current_url)
# 		header3 = self.browser.find_element_by_tag_name('h3').text
# 		self.assertIn('Books on hands:', header3)
# 		self.browser.implicitly_wait(1)
# 		print('Books on hands worked.')




# 		# Need return book
# 		general_button = self.browser.find_elements_by_xpath("//a[contains(text(), 'General Information')]")[0]
# 		general_button.click()

# 		menuItem = self.browser.find_element_by_link_text('Need return')
# 		menuItem.click()
# 		self.assertIn('http://localhost:8000/need-return-books', self.browser.current_url)
# 		header3 = self.browser.find_element_by_tag_name('h3').text
# 		self.assertIn('Need return these books (more than 14 days on hands):', header3)
# 		self.browser.implicitly_wait(1)
# 		print('Books on hands worked.')




# if __name__ == '__main__':
# 	unittest.main(warnings='ignore')