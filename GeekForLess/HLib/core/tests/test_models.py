from django.test import TestCase
from core.models import Genre


class TestModels(TestCase):

	@classmethod
	def setUpTestData(cls):
		Genre.objects.create(genre = 'Genre1')

	def test_genre_was_created(self):
		genre1=Genre.objects.get(id=1)
		self.assertTrue(isinstance(genre1, Genre))


	def test_genre_name_label(self):
		genre1=Genre.objects.get(id=1)
		field_label = genre1._meta.get_field('genre').verbose_name
		self.assertEquals(field_label, 'genre')


	def test_genre_check_STR(self):
		genre1=Genre.objects.get(id=1)
		self.assertEquals(genre1.__str__(), genre1.genre)

	def test_genre_max_length(self):
		genre1=Genre.objects.get(id=1)
		max_length = genre1._meta.get_field('genre').max_length
		self.assertEquals(max_length, 50)