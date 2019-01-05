from django.urls import path
from .views import (BooksListView,
					BooksOnHandsListView,
					BooksInLibraryListView,
					NeedReturnBookListView,
					# SearchView,
					# BooksInfoListView,
					BooksInfoDetailView,

					LocationListView,



					LocationCreateView, GenreCreateView, LocationUpdateView,
	)


urlpatterns = [
	path(r'', BooksListView.as_view(), name = 'base_view'),
	path(r'on_hands/', BooksOnHandsListView.as_view(), name = 'books-on-hands'),
	path(r'in_library/', BooksInLibraryListView.as_view(), name = 'books-in-library'),
	path(r'need_return/', NeedReturnBookListView.as_view(), name = 'need-return-book'),
	# path(r'search/', SearchView.as_view(), name = 'search_view'),


	# path(r'books_detail/', BooksInfoListView.as_view(), name = 'books_detail'),
	path(r'books_detail/<pk>-<title>/', BooksInfoDetailView.as_view(), name = 'book_unique_detail'),

	# locations
	path(r'location/', LocationListView.as_view(), name = 'location'),
	path(r'create_location/', LocationCreateView.as_view(), name = 'create_loc'),
	path(r'update_location/<room>-<bookcase>-<shelf>', LocationUpdateView.as_view(), name = 'update_loc'),
	# path(r'update_location/<pk>', LocationUpdateView.as_view(), name = 'update_loc'),

	path(r'create_genre/', GenreCreateView.as_view(), name = 'create_genre'),
]