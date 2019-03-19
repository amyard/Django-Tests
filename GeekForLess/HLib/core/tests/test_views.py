from django.test import TestCase, Client
from django.urls import reverse 
from core.models import Genre, Location, Person
import json


class TestViews(TestCase):

	def setUp(self):
		self.client = Client()

		self.base_url = reverse('base-view')
		self.books_on_hands = reverse('books-on-hands')
		self.books_in_library = reverse('books-in-library')
		self.need_return_book = reverse('need-return-books')


		# Let's test GENRE
		self.genre_listView = reverse('genre')
		self.genre1 = Genre.objects.create(genre = 'new awe genre')
		

		
	# GENETAL TESTS

	def test_base_view_listview_GET(self):		
		response = self.client.get(self.base_url)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, "core/main.html")

	def test_books_on_hands_listview_GET(self):		
		response = self.client.get(self.books_on_hands)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, "core/main.html")

	def test_books_in_library_listview_GET(self):		
		response = self.client.get(self.books_in_library)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, "core/main.html")

	def test_need_return_book_listview_GET(self):		
		response = self.client.get(self.need_return_book)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, "core/main.html")


###########################################################################
###########################    TEST GENRE     #############################
###########################################################################

class TestGenre(TestCase):

	@classmethod
	def setUpTestData(cls):

		# Create 25 genres for pagination tests
		number_of_genres = 25

		for genre_id in range(number_of_genres):
			Genre.objects.create(genre=f'Genre {genre_id}')


	def test_view_url_exists_at_desired_location(self):
		response = self.client.get('/genre')
		self.assertEqual(response.status_code, 200)


	def test_view_url_accessible_by_name(self):
		response = self.client.get(reverse('genre'))
		self.assertEqual(response.status_code, 200)

	def test_view_uses_correct_template(self):
		response = self.client.get(reverse('genre'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'core/detail.html')

	def test_pagination_is_twenty(self):
		response = self.client.get(reverse('genre'))
		self.assertEqual(response.status_code, 200)
		self.assertTrue('is_paginated' in response.context)
		self.assertTrue(response.context['is_paginated'] == True)
		self.assertTrue(len(response.context['categories']) == 20)

	def test_lists_all_authors(self):
        # Get second page and confirm it has exactly 5 items
		response = self.client.get(reverse('genre')+'?page=2')
		self.assertEqual(response.status_code, 200)
		self.assertTrue('is_paginated' in response.context)
		self.assertTrue(response.context['is_paginated'] == True)
		self.assertTrue(len(response.context['categories']) == 5)


	def test_genre_content(self):
		new_genre = Genre.objects.create(genre='Specific Genre')
		latest_genre = Genre.objects.latest('id')
		self.assertEqual(new_genre, latest_genre)

		expected_object_name = f'{new_genre.genre}'
		self.assertEquals(expected_object_name, 'Specific Genre')