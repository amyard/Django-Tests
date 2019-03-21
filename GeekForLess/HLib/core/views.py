from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import (Books, Genre, Location, Person, BookInfo, )
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from django.views import View
from datetime import date, timedelta

from .mixins import ListMixins, ListMixinAndCreate, CreateMixin, DeleteMixin, UpdateMixin
from django.db.models import Q, Sum, Count

from .forms import *

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


####################################################################################################
####################       GENERAL INFO ABOUT BOOKS AND THOSE POSITION       #######################
####################################################################################################


# All Books (in library+on hands)
class BooksListView(ListMixins, ListView):
	queryset = Books.objects.all().order_by('book')
	template_name = 'core/main.html'
	title = 'Main page'
	title_content = 'All books:'


# Books on hands
class BooksOnHandsListView(ListMixins, ListView):
	queryset = Books.objects.filter(Q(status_of_book = 1)|Q(status_of_book = -1))
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
class NeedReturnBookListView(ListMixins, ListView):
	queryset = Books.objects.filter(Q(date_of_return__lte = date.today())&Q(status_of_book = 1)|Q(status_of_book = -1))
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
	paginate_by = 10

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
		
		search_word = query.replace(' ', '+')

		p = Paginator(found_books, self.paginate_by)
		page_number = request.GET.get('page', 1)
		page = p.get_page(page_number)

		context = {
			'search_word': search_word,
			'books':page,
			'books_c':found_books,
			'title':self.title,
			'title_content':self.title_content
		}

		return render(self.request, self.template_name, context)



####################################################################################################
##################################      CREATE AND LISTVIEWS      ##################################
####################################################################################################


class BookDescription(ListMixinAndCreate, CreateMixin, ListView):
	model = BookInfo
	template_name = 'core/detail.html'
	form = BookInfoForm
	title = 'Book description'
	redirect_path = 'book-info'
	form_title = 'Add Book Description'
	form_buttom = 'Add info'
	paginate_by = 10
	sub_category = 'Book description'
	message_send = 'Book description was created successfully.'

				
class GenreDescription(ListMixinAndCreate, CreateMixin, ListView):
	model = Genre
	template_name = 'core/detail.html'
	form = GenreForm
	title = 'Genre'
	redirect_path = 'genre'
	form_title = 'Add New Genre'
	form_buttom = 'Add genre'
	paginate_by = 20
	sub_category = 'Genre'
	message_send = 'Genre was created successfully.'


class LocationDescription(ListMixinAndCreate, CreateMixin, ListView):
	model = Location
	template_name = 'core/detail.html'
	form = LocationForm
	title = 'Locations'
	redirect_path = 'locations'
	form_title = 'Add New Location'
	form_buttom = 'Add location'
	paginate_by = 20
	sub_category = 'Location'
	message_send = 'Location was created successfully.'


class PersonDescription(ListMixinAndCreate, CreateMixin, ListView):
	model = Person
	template_name = 'core/detail.html'
	form = PersonForm
	title = 'Subscribers'
	redirect_path = 'subscribers'
	form_title = 'Add New Person'
	form_buttom = 'Add person'
	paginate_by = 12
	sub_category = 'Subscriber'
	message_send = 'Subscriber was created successfully.'


class GeneralBookDescription(ListMixinAndCreate, CreateMixin, ListView):
	model = Books
	template_name = 'core/detail.html'
	form = BookForm
	title = 'Book status'
	redirect_path = 'general-book'
	form_title = 'Add New Book'
	form_buttom = 'Add book'
	paginate_by = 12
	sub_category = 'General Info'
	message_send = 'General Info was created successfully.'



####################################################################################################
##################################          DELETE VIEWS          ##################################
####################################################################################################


class GenreDelete(DeleteMixin, DeleteView):
	model = Genre

class BookInfoDelete(DeleteMixin, DeleteView):
	model = BookInfo

class LocationDelete(DeleteMixin, DeleteView):
	model = Location

class PersonDelete(DeleteMixin, DeleteView):
	model = Person

class GeneralBookDelete(DeleteMixin, DeleteView):
	model = Books

	

####################################################################################################
##################################          UPDATE VIEWS          ##################################
####################################################################################################

class GenreUpdate(UpdateMixin, View):
	model = Genre
	template_name = 'core/detail.html'
	form = GenreForm
	title = 'Genre'
	form_title = 'Edit Genre'
	paginate_by = 20
	sub_category = 'Genre'
	message_send = 'Genre was updated successfully.'


class BookUpdate(UpdateMixin, View):
	model = BookInfo
	template_name = 'core/detail.html'
	form = BookInfoFormUpdate
	title = 'Book description:'
	form_title = 'Edit Book Description'
	paginate_by = 10
	sub_category = 'Book description'
	message_send = 'Book was updated successfully.'


class LocationUpdate(UpdateMixin, View):
	model = Location
	template_name = 'core/detail.html'
	form = LocationForm
	title = 'Location description:'
	form_title = 'Edit Location'
	paginate_by = 20
	sub_category = 'Location'
	message_send = 'Location was updated successfully.'



class PersonUpdate(UpdateMixin, View):
	model = Person
	template_name = 'core/detail.html'
	form = PersonForm
	title = 'Subscriber description:'
	form_title = 'Edit Subscriber'
	paginate_by = 12
	sub_category = 'Subscriber'
	message_send = 'Subscriber was updated successfully.'


class GeneralBookUpdate(UpdateMixin, View):
	model = Books
	template_name = 'core/detail.html'
	form = BookFormUpdate
	title = 'General information'
	form_title = 'Edit Book'
	paginate_by = 12
	sub_category = 'General Info'
	message_send = 'General Info was updated successfully.'



####################################################################################################
##################################          UNIQUE BOOK           ##################################
####################################################################################################


class BooksInfoDetailView(DetailView):
	model = Books
	template_name = 'core/unique-book.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BooksInfoDetailView, self).get_context_data(*args, **kwargs)
		context['title'] = self.kwargs.get('book')
		context['book'] = self.get_object()

		return context


####################################################################################################
##################################          Statistics            ##################################
####################################################################################################


class StatisticListView(ListView):
	model = Books
	template_name = 'core/statistics.html'
	title = 'Statistics'

	def get_context_data(self, *args, **kwargs):
		context = super(StatisticListView, self).get_context_data(*args, **kwargs)
		context['title'] = self.title
		context['today'] = date.today()
		context['statistics'] = self.model.objects.all().order_by('-date_of_issue')
		context['uniq_vals'] = self.model.objects.values('date_of_issue').distinct().order_by('-date_of_issue')
		context['count_vals'] = self.model.objects.values('date_of_issue', 'status_of_book').order_by('-date_of_issue').annotate(Count('status_of_book'))
		context['general_count'] = self.model.objects.values('date_of_issue').order_by('-date_of_issue').annotate(Count('status_of_book'))

		return context