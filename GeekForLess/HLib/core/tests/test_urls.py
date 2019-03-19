from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import (BooksListView, BooksOnHandsListView, BooksInLibraryListView, NeedReturnBookListView,
	BooksInfoDetailView, StatisticListView, SearchView, 
	BookDescription, GenreDescription, LocationDescription, PersonDescription, GeneralBookDescription,
	BookInfoDelete, GenreDelete, LocationDelete, PersonDelete, GeneralBookDelete,
	GenreUpdate, BookUpdate, LocationUpdate, PersonUpdate, GeneralBookUpdate, )




class TestUrls(SimpleTestCase):

	def test_base_view_resolve(self):
		url = reverse('base-view')
		print(resolve(url))
		# for func
		# self.assertEqual(resolve(url).func, BooksListView)

		# for class
		self.assertEqual(resolve(url).func.view_class, BooksListView)

	def test_books_on_hands_resolve(self):
		url = reverse('books-on-hands')
		self.assertEqual(resolve(url).func.view_class, BooksOnHandsListView)

	def test_books_in_library_resolve(self):
		url = reverse('books-in-library')
		self.assertEqual(resolve(url).func.view_class, BooksInLibraryListView)

	def test_need_return_book_resolve(self):
		url = reverse('need-return-books')
		self.assertEqual(resolve(url).func.view_class, NeedReturnBookListView)

	def test_detail_book(self):
		url = reverse('unique-book', args=['1', 'Title 1'])
		self.assertEqual(resolve(url).func.view_class, BooksInfoDetailView)

	def test_statistics(self):
		url = reverse('statistics')
		self.assertEqual(resolve(url).func.view_class, StatisticListView)

	def test_search_view(self):
		url = reverse('search-view')
		self.assertEqual(resolve(url).func.view_class, SearchView)



	# DETAIL

	def test_book_info_detail_view(self):
		url = reverse('book-info')
		self.assertEqual(resolve(url).func.view_class, BookDescription)

	def test_genre_detail_view(self):
		url = reverse('genre')
		self.assertEqual(resolve(url).func.view_class, GenreDescription)

	def test_location_detail_view(self):
		url = reverse('locations')
		self.assertEqual(resolve(url).func.view_class, LocationDescription)

	def test_subscriber_detail_view(self):
		url = reverse('subscribers')
		self.assertEqual(resolve(url).func.view_class, PersonDescription)

	def test_general_info_about_book_detail_view(self):
		url = reverse('general-book')
		self.assertEqual(resolve(url).func.view_class, GeneralBookDescription)




	# DELETE

	def test_delete_book_info(self):
		url = reverse('delete-book-info', args=[1])
		self.assertEqual(resolve(url).func.view_class, BookInfoDelete)

	def test_delete_genre(self):
		url = reverse('delete-genre', args=[1])
		self.assertEqual(resolve(url).func.view_class, GenreDelete)

	def test_delete_location(self):
		url = reverse('delete-location', args=[1])
		self.assertEqual(resolve(url).func.view_class, LocationDelete)

	def test_delete_subscriber(self):
		url = reverse('delete-person', args=[1])
		self.assertEqual(resolve(url).func.view_class, PersonDelete)

	def test_delete_general_info_about_book(self):
		url = reverse('delete-general-book', args=[1])
		self.assertEqual(resolve(url).func.view_class, GeneralBookDelete)



	# UPDATE

	def test_update_book_info(self):
		url = reverse('update-book-info', args=[1])
		self.assertEqual(resolve(url).func.view_class, BookUpdate)

	def test_update_genre(self):
		url = reverse('update-genre', args=[1])
		self.assertEqual(resolve(url).func.view_class, GenreUpdate)

	def test_update_location(self):
		url = reverse('update-locations', args=[1])
		self.assertEqual(resolve(url).func.view_class, LocationUpdate)

	def test_update_subscriber(self):
		url = reverse('update-subscribers', args=[1])
		self.assertEqual(resolve(url).func.view_class, PersonUpdate)

	def test_update_general_info_about_book(self):
		url = reverse('update-general-book', args=[1])
		self.assertEqual(resolve(url).func.view_class, GeneralBookUpdate)
