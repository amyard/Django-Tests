from django.urls import path
from .views import *



urlpatterns = [
    path('', BooksListView.as_view(), name = 'base-view'),
    path('books-on-hands', BooksOnHandsListView.as_view(), name = 'books-on-hands'),
    path('books-in-library', BooksInLibraryListView.as_view(), name = 'books-in-library'),
    path('need-return-books', NeedReturnBookListView.as_view(), name = 'need-return-books'),
    path(r'search', SearchView.as_view(), name = 'search-view'),


    # Detail and Create Views
    path(r'book-info', BookDescription.as_view(), name = 'book-info'),
    path(r'genre', GenreDescription.as_view(), name = 'genre'),
    path(r'locations', LocationDescription.as_view(), name = 'locations'),
    path(r'subscribers', PersonDescription.as_view(), name = 'subscribers'),
    path(r'general-book', GeneralBookDescription.as_view(), name = 'general-book'),

    
]