# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import unittest



# class IndexTestCase(unittest.TestCase):

# 	def setUp(self):
# 		self.browser = webdriver.Firefox()
# 		self.browser.get('http://localhost:8000')
# 		self.browser.implicitly_wait(2)

# 	def tearDown(self):
# 		self.browser.quit()



# 	def test_base_view(self):

# 		# current url
# 		self.assertIn('http://localhost:8000', self.browser.current_url)
# 		print('current url - done.')


# 		# check logo
# 		logo = self.browser.find_element_by_css_selector('.navbar-brand')
# 		self.assertIn('Library Helper', logo.text)
# 		print('Logo - done.')


# 		# check title of page
# 		self.assertEqual(self.browser.title, 'Main page - Library Helper')
# 		print('Title - done.')

# 		# check header of table
# 		header3 = self.browser.find_element_by_tag_name('h3').text
# 		self.assertIn('All books:', header3)
# 		print('Header - done.')


# 		# Search form
# 		search_box = self.browser.find_element_by_class_name('search-form')
# 		self.assertEqual(search_box.get_attribute('placeholder'),
# 			'Search by title or subscriber')
# 		print('Search box placeholder - done.')
		

# if __name__ == '__main__':
# 	unittest.main(warnings='ignore')