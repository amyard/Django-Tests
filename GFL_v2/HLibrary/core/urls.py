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

    
    # Delete Views
    path(r'delete/book-info/<pk>', BookInfoDelete.as_view(), name = 'delete-book-info'),
    path(r'delete/genre/<pk>', GenreDelete.as_view(), name = 'delete-genre'),
    path(r'delete/location/<pk>', LocationDelete.as_view(), name = 'delete-location'),
    path(r'delete/person/<pk>', PersonDelete.as_view(), name = 'delete-person'),
    path(r'delete/general-book/<pk>', GeneralBookDelete.as_view(), name = 'delete-general-book'),

    # Update
    path(r'update/genre/<pk>', GenreUpdate.as_view(), name = 'update-genre'),
    path(r'update/book-info/<pk>', BookUpdate.as_view(), name = 'update-book-info'),    
    path(r'update/locations/<pk>', LocationUpdate.as_view(), name = 'update-locations'),
    path(r'update/subscribers/<pk>', PersonUpdate.as_view(), name = 'update-subscribers'),
    path(r'update/general-book/<pk>', GeneralBookUpdate.as_view(), name = 'update-general-book'),

]

GeneralBookUpdate

