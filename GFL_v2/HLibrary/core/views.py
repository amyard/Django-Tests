from django.shortcuts import render
from django.http import HttpResponse
from .models import (Books, Genre, Location, Person, BookInfo, )
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.views import View
from datetime import date, timedelta

from .mixins import ListMixins
from django.db.models import Q


####################################################################################################
####################       GENERAL INFO ABOUT BOOKS AND THOSE POSITION       #######################
####################################################################################################


# All Books (in library+on hands)
class BooksListView(ListMixins, ListView):
	queryset = Books.objects.all()
	template_name = 'core/main.html'
	title = 'Main page'
	title_content = 'All books:'


# Books on hands
class BooksOnHandsListView(ListMixins, ListView):
	queryset = Books.objects.filter(
							Q(date_of_issue__lte = date.today() - timedelta(days=14))|
							Q(status_of_book = 1))
	template_name = 'core/main.html'
	title = 'Main page'
	title_content = 'Books on hands:'


# Books in library
class BooksInLibraryListView(ListMixins, ListView):
	queryset = Books.objects.filter(status_of_book = 0)
	template_name = 'core/main.html'
	title = 'Main page'
	title_content = 'Books in library:'


# This books need to return
class NeedReturnBookListView(ListView):
	queryset = Books.objects.filter(
							Q(date_of_issue__lte = date.today() - timedelta(days=14))|
							Q(status_of_book = -1))
	template_name = 'core/main.html'
	title = 'Main page'
	title_content = 'Need return these books (more than 14 days on hands):'



####################################################################################################
########################################       SEARCH       ########################################
####################################################################################################


class SearchView(View):
	template_name='core/main.html'
	title = 'Search'
	model = Books
	title_content = 'Founded information'

	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('q')

		if len(query.split(' ')) == 1:
			found_books = self.model.objects.filter(
								Q(book__title__icontains = query)|
								Q(person_subscription__lastname__icontains = query)|
								Q(person_subscription__firstname__icontains = query)
							)
		else:
			found_books = self.model.objects.filter(
								Q(book__title__icontains = query)|
								Q(person_subscription__lastname__icontains = query.split(' ')[0])|
								Q(person_subscription__firstname__icontains = query.split(' ')[1])
							)

		context = {
			'found_books':found_books,
			'title':self.title,
			'title_content':self.title_content
		}

		return render(self.request, self.template_name, context)