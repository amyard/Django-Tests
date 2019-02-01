from django.urls import path
from .views import *



urlpatterns = [
    path('', BooksListView.as_view(), name = 'base-view'),
    path('books-on-hands', BooksOnHandsListView.as_view(), name = 'books-on-hands'),
    path('books-in-library', BooksInLibraryListView.as_view(), name = 'books-in-library'),
    path('need-return-books', NeedReturnBookListView.as_view(), name = 'need-return-books'),
]
