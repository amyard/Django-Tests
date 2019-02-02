from django.urls import path
from .views import *



urlpatterns = [
    path('', BooksListView.as_view(), name = 'base-view'),
    path('books-on-hands', BooksOnHandsListView.as_view(), name = 'books-on-hands'),
    path('books-in-library', BooksInLibraryListView.as_view(), name = 'books-in-library'),
    path('need-return-books', NeedReturnBookListView.as_view(), name = 'need-return-books'),
    path('search', SearchView.as_view(), name = 'search-view'),


    # Detail and Create Views
    path('book-info', BookDescription.as_view(), name = 'book-info'),
    path('genre', GenreDescription.as_view(), name = 'genre'),
    path('locations', LocationDescription.as_view(), name = 'locations'),
    path('subscribers', PersonDescription.as_view(), name = 'subscribers'),
    path('general-book', GeneralBookDescription.as_view(), name = 'general-book'),

    
    # Delete Views
    path('delete/book-info/<pk>', BookInfoDelete.as_view(), name = 'delete-book-info'),
    path('delete/genre/<pk>', GenreDelete.as_view(), name = 'delete-genre'),
    path('delete/location/<pk>', LocationDelete.as_view(), name = 'delete-location'),
    path('delete/person/<pk>', PersonDelete.as_view(), name = 'delete-person'),
    path('delete/general-book/<pk>', GeneralBookDelete.as_view(), name = 'delete-general-book'),

    # Update
    path('update/genre/<pk>', GenreUpdate.as_view(), name = 'update-genre'),
    path('update/book-info/<pk>', BookUpdate.as_view(), name = 'update-book-info'),    
    path('update/locations/<pk>', LocationUpdate.as_view(), name = 'update-locations'),
    path('update/subscribers/<pk>', PersonUpdate.as_view(), name = 'update-subscribers'),
    path('update/general-book/<pk>', GeneralBookUpdate.as_view(), name = 'update-general-book'),

    # Detail by book
    path('book/<pk>-<book>', BooksInfoDetailView.as_view(), name='unique-book'),

    # Statistics
    path('statistics', StatisticListView.as_view(), name = 'statistics')

]

GeneralBookUpdate

