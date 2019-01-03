from django.urls import path
from .views import (BooksListView,
					BooksOnHandsListView,
					BooksInLibraryListView,
					SearchView,
					BooksInfoListView,
					BooksInfoDetailView,
	)


urlpatterns = [
	path(r'', BooksListView.as_view(), name = 'base_view'),
	path(r'on_hands/', BooksOnHandsListView.as_view(), name = 'books-on-hands'),
	path(r'in_library/', BooksInLibraryListView.as_view(), name = 'books-in-library'),
	path(r'search/', SearchView.as_view(), name = 'search_view'),


	path(r'books_detail/', BooksInfoListView.as_view(), name = 'books_detail'),
	path(r'books_detail/<pk>-<title>/', BooksInfoDetailView.as_view(), name = 'book_unique_detail'),

]