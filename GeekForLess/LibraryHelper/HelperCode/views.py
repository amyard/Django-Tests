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
	)


# Create your views here.
class BooksListView(ListView):
	model = Books
	template_name = 'index.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BooksListView, self).get_context_data(*args, **kwargs)
		context['books'] = self.model.objects.all()
		
		return context


class BooksOnHandsListView(ListView):
	model = Books
	template_name = 'books_on_hands.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BooksOnHandsListView, self).get_context_data(*args, **kwargs)
		context['books_on_hands'] = self.model.objects.filter(status_of_book = 1)

		return context


class BooksInLibraryListView(ListView):
	model = Books
	template_name = 'books_in_library.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BooksInLibraryListView, self).get_context_data(*args, **kwargs)
		context['books_in_library'] = self.model.objects.filter(status_of_book = 0)

		return context


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


# # for search form
# class SearchView(View):
# 	template_name='search.html'

# 	def get(self, request, *args, **kwargs):
# 		query = self.request.GET.get('q')
# 		fonded_books = Books.objects.filter(
# 								Q(book__icontains = query)
# 							)

# 		context = {
# 			'fonded_books':fonded_books
# 		}

# 		return render(self.request, self.template_name, context)




# # BooksInformation 

# class BooksInfoListView(ListView):
# 	model = BookInfo
# 	template_name = 'books_detail.html'

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(BooksInfoListView, self).get_context_data(*args, **kwargs)
# 		context['booksinfo'] = self.model.objects.all()
		
# 		return context



class BooksInfoDetailView(DetailView):
	model = Books
	template_name = 'book_unique_detail.html'

	def get_context_data(self, *args, **kwargs):
		context = super(BooksInfoDetailView, self).get_context_data(*args, **kwargs)
		context['book'] = self.get_object()

		return context 




# ALL Locations
class LocationListView(ListView):
	model = Location
	template_name = 'location.html'

	def get_context_data(self, *args, **kwargs):
		context = super(LocationListView, self).get_context_data(*args, **kwargs)
		context['locations'] = self.model.objects.all()

		return context

# Create viewS
class LocationCreateView(CreateView):
	template_name = 'create.html'
	form_class = LocationForm
	queryset = Location.objects.all()
	success_url = '/location/'

	def form_valid(self, form):
		print(form.cleaned_data)
		return super().form_valid(form)


# Update viewS
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
		# print(form.cleaned_data)
		# instance = form.save(commit=False)
		return super(LocationUpdateView, self).form_valid(form)







####################################################################################
####################################################################################

class GenreCreateView(CreateView):
	template_name = 'create.html'
	form_class = GenreForm
	queryset = Genre.objects.all()
	success_url = '/'

	def form_valid(self, form):
		print(form.cleaned_data)
		return super().form_valid(form)