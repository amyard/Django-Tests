from django.test import SimpleTestCase
from core.forms import LocationForm



class TestForms(SimpleTestCase):
	def test_form_location_is_valid(self):
		form = LocationForm(data = {
			'room': 45454545,
			'bookcase': 45454545,
			'shelf': 45454545
			})

		self.assertTrue(form.is_valid())

	def test_form_location_no_data(self):
		form = LocationForm(data = {})
		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors),3)