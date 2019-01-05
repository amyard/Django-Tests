from django.urls import path
from .views import (BooksListView,
					BooksOnHandsListView,
					BooksInLibraryListView,
					NeedReturnBookListView,
					SearchView,
					BooksInfoDetailView,
					StatisticListView,
					LocationListView,


					LocationCreateView, GenreCreateView, LocationUpdateView,
					GenreListView, GenreCreateView, GenreUpdateView,
					PersonListView, PersonCreateView, PersonUpdateView,
					BookInfoListView, BookInfoCreateView, BookInfoUpdateView,
					GeneralBookListView, GeneralBookCreateView, GeneralBookUpdateView,
	)


urlpatterns = [
	path(r'', BooksListView.as_view(), name = 'base_view'),
	path(r'on_hands/', BooksOnHandsListView.as_view(), name = 'books-on-hands'),
	path(r'in_library/', BooksInLibraryListView.as_view(), name = 'books-in-library'),
	path(r'need_return/', NeedReturnBookListView.as_view(), name = 'need-return-book'),
	path(r'search/', SearchView.as_view(), name = 'search_view'),

	path(r'statistics/', StatisticListView.as_view(), name = 'statistics'),

	path(r'books_detail/<pk>-<title>/', BooksInfoDetailView.as_view(), name = 'book_unique_detail'),

	# locations
	path(r'location/', LocationListView.as_view(), name = 'location'),
	path(r'create_location/', LocationCreateView.as_view(), name = 'create_loc'),
	path(r'update_location/<room>-<bookcase>-<shelf>', LocationUpdateView.as_view(), name = 'update_loc'),

	# genre
	path(r'genre/', GenreListView.as_view(), name = 'genre'),
	path(r'create_genre/', GenreCreateView.as_view(), name = 'create_genre'),
	path(r'update_genre/<title>', GenreUpdateView.as_view(), name = 'update_genre'),

	# person
	path(r'person/', PersonListView.as_view(), name = 'person'),
	path(r'create_person/', PersonCreateView.as_view(), name = 'create_person'),
	path(r'update_person/<lastname>-<firstname>/', PersonUpdateView.as_view(), name = 'update_person'),

	# bookinfo
	path(r'book_info/', BookInfoListView.as_view(), name = 'book_info'),
	path(r'create_book_info/', BookInfoCreateView.as_view(), name = 'create_book_info'),
	path(r'update_book_info/<title>/', BookInfoUpdateView.as_view(), name = 'update_book_info'),

	# bookinfo
	path(r'main_info/', GeneralBookListView.as_view(), name = 'general_book_info'),
	path(r'create_general_book/', GeneralBookCreateView.as_view(), name = 'create_general_book'),
	path(r'update_general_book/<book>', GeneralBookUpdateView.as_view(), name = 'update_general_book'),


]