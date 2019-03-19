from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from django.urls import reverse
from core.models import Location




class IndexTestCase(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.get('http://localhost:8000')
		self.browser.implicitly_wait(2)
		self.action_button = self.browser.find_elements_by_xpath("//a[contains(text(), 'Actions')]")[0]
		self.action_button.click()
		self.menuItem = self.browser.find_element_by_link_text('Location')
		self.menuItem.click()

	def tearDown(self):
		self.browser.quit()


	# def test_location_current_url(self):
	# 	self.assertIn('http://localhost:8000/locations', self.browser.current_url)


	# def test_location_paggination(self):
	# 	last_pag = self.browser.find_elements_by_xpath("//a[contains(text(), 'Last')]")[-1]
	# 	last_pag.click()
	# 	link_numb = self.browser.current_url.split('?page=')[-1]
	# 	self.assertEqual(int(link_numb), 2)


	# def test_location_create(self):
	# 	pos_count = len(Location.objects.filter())
	# 	print(pos_count)
	# 	test_position = 1
	# 	room = self.browser.find_element_by_id('id_room').send_keys(test_position)
	# 	bookcase = self.browser.find_element_by_id('id_bookcase').send_keys(test_position)
	# 	shelf = self.browser.find_element_by_id('id_shelf').send_keys(test_position)
	# 	self.browser.find_elements_by_xpath("//*[contains(text(), 'Add location')]")[0].click()


	def test_location_update(self):
		sect = self.browser.find_elements_by_class_name('caption')[0]
		update_button = sect.find_element_by_xpath("//a[contains(text(), 'Update')]")
		update_button.click()
		print('COOOLLLLL')