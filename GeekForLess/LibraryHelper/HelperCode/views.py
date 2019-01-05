from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from django.shortcuts import redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import (Books,
					Genre,
					Location,
					Person,
					BookInfo
	)


# for search view
from django.db.models import Q
from django.views import View

from datetime import date, timedelta


from .forms import (LocationForm,
					GenreForm,
					PersonForm, PersonUpdateForm,
					BookInfoForm, BookUpdateInfoForm,
					BookForm,
	)


# Create your views here
# All Books (in library+on hands)
class BooksListView(ListView):
	model = Books
	template_name = 'index.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BooksListView, self).get_context_data(*args, **kwargs)
		context['books'] = self.model.objects.all()
		
		return context


# Books on hands
class BooksOnHandsListView(ListView):
	model = Books
	template_name = 'books_on_hands.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BooksOnHandsListView, self).get_context_data(*args, **kwargs)
		
		date_period = date.today() - timedelta(days=14)
		context['books_on_hands'] = self.model.objects.filter(
							Q(date_of_issue__lte = date_period)|
							Q(status_of_book = 1)
			)

		return context


# Books in library
class BooksInLibraryListView(ListView):
	model = Books
	template_name = 'books_in_library.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BooksInLibraryListView, self).get_context_data(*args, **kwargs)
		context['books_in_library'] = self.model.objects.filter(status_of_book = 0)

		return context


# This books need to return
class NeedReturnBookListView(ListView):
	model = Books
	template_name = 'need_return_book.html'

	def get_context_data(self, *args, **kwargs):
		context = super(NeedReturnBookListView, self).get_context_data(*args, **kwargs)
		#context['need_return_book'] = self.model.objects.filter(status_of_book = -1)

		date_period = date.today() - timedelta(days=14)
		context['need_return_book'] = self.model.objects.filter(
							Q(date_of_issue__lte = date_period)|
							Q(status_of_book = -1)
			)

		return context


# for search form
class SearchView(View):
	template_name='search.html'

	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('q')

		if len(query.split(' ')) == 1:
			fonded_books = Books.objects.filter(
								Q(book__title__icontains = query)|
								Q(person_subscription__lastname__icontains = query)|
								Q(person_subscription__firstname__icontains = query)
							)
		else:
			fonded_books = Books.objects.filter(
								Q(book__title__icontains = query)|
								Q(person_subscription__lastname__icontains = query.split(' ')[0])|
								Q(person_subscription__firstname__icontains = query.split(' ')[1])
							)

		context = {
			'fonded_books':fonded_books
		}

		return render(self.request, self.template_name, context)





# # BooksInformation 

class BooksInfoDetailView(DetailView):
	model = Books
	template_name = 'book_unique_detail.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BooksInfoDetailView, self).get_context_data(*args, **kwargs)
		context['book'] = self.get_object()

		return context 



#######################################################################################
####################            LOCATIONS IN LIBRARY         ##########################
#######################################################################################



# ALL Locations
class LocationListView(ListView):
	model = Location
	template_name = 'location.html'

	def get_context_data(self, *args, **kwargs):
		context = super(LocationListView, self).get_context_data(*args, **kwargs)
		context['locations'] = self.model.objects.all()

		return context


class LocationCreateView(CreateView):
	template_name = 'create.html'
	form_class = LocationForm
	queryset = Location.objects.all()
	success_url = '/location/'

	def form_valid(self, form):
		print(form.cleaned_data)
		return super().form_valid(form)


class LocationUpdateView(UpdateView):
	template_name = 'create.html'
	form_class = LocationForm
	queryset = Location.objects.all()
	success_url = '/location/'

	def get_object(self, *args, **kwargs):
		room_ = self.kwargs.get('room')
		bookcase_ = self.kwargs.get('bookcase')
		shelf_ = self.kwargs.get('shelf')

		return get_object_or_404(Location, room = room_, bookcase = bookcase_, shelf = shelf_)


	def form_valid(self, form):
		print(form.cleaned_data)
		return super(LocationUpdateView, self).form_valid(form)







#######################################################################################
####################                  GENRE                  ##########################
#######################################################################################


class GenreListView(ListView):
	model = Genre
	template_name = 'genre.html'

	def get_context_data(self, *args, **kwargs):
		context = super(GenreListView, self).get_context_data(*args, **kwargs)
		context['genres'] = self.model.objects.all()

		return context


class GenreCreateView(CreateView):
	template_name = 'create.html'
	form_class = GenreForm
	queryset = Genre.objects.all()
	success_url = '/genre/'

	def form_valid(self, form):
		print(form.cleaned_data)
		return super(GenreCreateView, self).form_valid(form)




class GenreUpdateView(UpdateView):
	template_name = 'create.html'
	form_class = GenreForm
	queryset = Genre.objects.all()
	success_url = '/genre/'

	def get_object(self, *args, **kwargs):
		title_ = self.kwargs.get('title')
		return get_object_or_404(Genre, title = title_)


	def form_valid(self, form):
		print(form.cleaned_data)
		return super(GenreUpdateView, self).form_valid(form)



#######################################################################################
####################                  Subscriber             ##########################
#######################################################################################


class PersonListView(ListView):
	model = Person
	template_name = 'subscriber.html'

	def get_context_data(self, *args, **kwargs):
		context = super(PersonListView, self).get_context_data(*args, **kwargs)
		context['subscribers'] = self.model.objects.all()

		return context


class PersonCreateView(CreateView):
	template_name = 'create.html'
	form_class = PersonForm
	queryset = Person.objects.all()
	success_url = '/person/'

	def form_valid(self, form):
		print(form.cleaned_data)
		return super(PersonCreateView, self).form_valid(form)




class PersonUpdateView(UpdateView):
	template_name = 'create.html'
	form_class = PersonUpdateForm
	queryset = Person.objects.all()
	success_url = '/person/'

	def get_object(self, *args, **kwargs):
		lastname_ = self.kwargs.get('lastname')
		firstname_ = self.kwargs.get('firstname')
		return get_object_or_404(Person, lastname = lastname_, firstname = firstname_)


	def form_valid(self, form):
		print(form.cleaned_data)
		return super(PersonUpdateView, self).form_valid(form)



#######################################################################################
####################                  Book Info              ##########################
#######################################################################################


class BookInfoListView(ListView):
	model = BookInfo
	template_name = 'bookinfo.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BookInfoListView, self).get_context_data(*args, **kwargs)
		context['infos'] = self.model.objects.all().order_by('-pk')

		return context


class BookInfoCreateView(CreateView):
	template_name = 'create.html'
	form_class = BookInfoForm
	queryset = BookInfo.objects.all()
	success_url = '/book_info/'

	def form_valid(self, form):
		print(form.cleaned_data)
		return super(BookInfoCreateView, self).form_valid(form)




class BookInfoUpdateView(UpdateView):
	template_name = 'create.html'
	form_class = BookUpdateInfoForm
	queryset = BookInfo.objects.all()
	success_url = '/book_info/'

	def get_object(self, *args, **kwargs):
		title_ = self.kwargs.get('title')
		return get_object_or_404(BookInfo, title = title_)


	def form_valid(self, form):
		print(form.cleaned_data)
		return super(BookInfoUpdateView, self).form_valid(form)




#######################################################################################
####################          General Book Info              ##########################
#######################################################################################


class GeneralBookListView(ListView):
	model = Books
	template_name = 'generalbookinfo.html'

	def get_context_data(self, *args, **kwargs):
		context = super(GeneralBookListView, self).get_context_data(*args, **kwargs)
		context['general_info'] = self.model.objects.all().order_by('-pk')

		return context


class GeneralBookCreateView(CreateView):
	template_name = 'create.html'
	form_class = BookForm
	queryset = Books.objects.all()
	success_url = '/main_info/'

	def form_valid(self, form):
		print(form.cleaned_data)
		return super().form_valid(form)




class GeneralBookUpdateView(UpdateView):
	template_name = 'create.html'
	form_class = BookForm
	queryset = Books.objects.all()
	success_url = '/main_info/'

	def get_object(self, *args, **kwargs):
		book_ = self.kwargs.get('book')
		return get_object_or_404(Books, book__title=book_)


	def form_valid(self, form):
		print(form.cleaned_data)
		return super(GeneralBookUpdateView, self).form_valid(form)