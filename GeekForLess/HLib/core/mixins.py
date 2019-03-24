from datetime import date, timedelta
from .models import (Books, Genre, Location, Person, BookInfo, )
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages


import operator
from functools import reduce



##########################################################################################
#######################            LIST VIEWS FOR GENERAL PAGE      ######################
##########################################################################################


class ListMixins():
	model = None
	template_name = None
	title = None
	title_content = None
	paginate_by = 10


	def get_queryset(self):
		return self.model.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		p = Paginator(self.get_queryset(), self.paginate_by)
		context['books'] = p.page(context['page_obj'].number)
		context['title'] = self.title
		context['title_content'] = self.title_content

		# Display Messages on main page
		# Books were returned, but still have position (0,0,0)
		ids = self.model.objects.filter(status_of_book=0).values_list('book_id', flat = True)
		context['returned_book_without_position'] = BookInfo.objects.filter(reduce(operator.or_, [Q(id = x)&Q(position__room=0)&Q(position__bookcase=0)&Q(position__shelf=0) for x in ids]))
		
		# Books which were only created and didn't added to the Books model with status 'In Library'
		ids = Books.objects.all().values_list('book_id', flat = True)
		context['never_used_books'] = BookInfo.objects.exclude(pk__in = ids)

		return context



##########################################################################################
#######################             DETAIL AND CREATE VIEWS         ######################
##########################################################################################


class ListMixinAndCreate():
	model = None
	template_name = None
	form = None
	title = None
	redirect_path = None
	form_title = None
	form_buttom = None
	paginate_by = None
	sub_category = None
	message_send = None


	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		qs = self.model.objects.select_related().all()
		p = Paginator(qs, self.paginate_by)
		context['categories'] = p.page(context['page_obj'].number)
		context['form'] = self.form
		context['title'] = self.title
		context['form_title'] = self.form_title
		context['form_buttom'] = self.form_buttom
		context['sub_category'] = self.sub_category

		# IF BOOK IF ON HANDS for url 'book-info' -> Info about Book
		context['position_of_book'] = Books.objects.filter(Q(status_of_book = -1)|Q(status_of_book = 1)).values_list('book__title', flat=True)

		# Books were returned, but still have position (0,0,0)
		ids = Books.objects.filter(status_of_book=0).values_list('book_id', flat = True)
		context['returned_book_without_position'] = BookInfo.objects.filter(reduce(operator.or_, [Q(id = x)&Q(position__room=0)&Q(position__bookcase=0)&Q(position__shelf=0) for x in ids]))

		# Books which were only created and didn't added to the Books model with status 'In Library'
		ids = Books.objects.all().values_list('book_id', flat = True)
		context['never_used_books'] = BookInfo.objects.exclude(pk__in = ids)
		
		return context



class CreateMixin():

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			form.save()

			# Изменение логики программы
			if request.resolver_match.func.__name__ == 'GeneralBookDescription':
				stat = form.cleaned_data['status_of_book']
				if stat == 1 or stat == -1:
					BookInfo.objects.filter(title=Books.objects.first()).update(position=Location.objects.get(id=32))

			messages.success(self.request, self.message_send)
			return HttpResponseRedirect(self.redirect_path)

		context = {'form': form, 'categories': self.model.objects.all(), 'title': self.title, 'form_title': self.form_title, 
				   'form_buttom': self.form_buttom, 'sub_category': self.sub_category}
		return render(self.request, self.template_name, context)



##########################################################################################
################################             DELETE VIEWS       ##########################
##########################################################################################

class DeleteMixin():
	model = None

	def get(self, *args, **kwargs):
		return self.post(*args, **kwargs)

	def get_success_url(self, **kwargs):
		return self.request.META.get('HTTP_REFERER')


####################################################################################################
##################################          UPDATE VIEWS          ##################################
####################################################################################################

class UpdateMixin():
	model = None
	template_name = None
	form = None
	title = None
	form_title = None
	form_buttom = 'Save'
	paginate_by = None
	sub_category = None
	message_send = None
	cancel_button = None

	def get(self, request, **kwargs):
		pk = self.kwargs.get('pk')
		categories = get_object_or_404(self.model, pk=pk)
		form = self.form(instance = categories)
		self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')

		# отображает страницу, где находится данный атрибут
		p = Paginator(self.model.objects.all(), self.paginate_by)
		if '?page=' in self.request.session['report_url']:
			num = self.request.session['report_url'].split('?page=')[-1]
		else:
			num = 1
		page_number = request.GET.get('page', num)
		page = p.get_page(page_number)
		return render(request, self.template_name, context = {'form': form, 'categories': page, 'cancel_button':self.cancel_button,
															  'title': self.title, 'form_title': self.form_title, 
				   											  'form_buttom': self.form_buttom, 'sub_category': self.sub_category})



	def post(self, request, **kwargs):
		pk = self.kwargs.get('pk')
		categories = get_object_or_404(self.model, pk=pk)
		form = self.form(request.POST, instance = categories)	
		if form.is_valid():
			form.save()

			# Изменение логики программы
			if request.resolver_match.func.__name__ == 'GeneralBookUpdate':
				stat = form.cleaned_data['status_of_book']
				if stat == 1 or stat == -1:
					book_id = categories.book.id
					BookInfo.objects.filter(id=book_id).update(position=Location.objects.get(id=32))

			messages.success(self.request, self.message_send)
			return HttpResponseRedirect(self.request.session.get('report_url'))



		# отображает страницу, где находится данный атрибут
		p = Paginator(self.model.objects.all(), self.paginate_by)
		if '?page=' in self.request.META.get('HTTP_REFERER'):
			num = self.request.META.get('HTTP_REFERER').split('?page=')[-1]
		else:
			num = 1
		page_number = request.GET.get('page', num)
		page = p.get_page(page_number)

		return render(request, self.template_name, context = {'form': form, 'categories': page, 'cancel_button':self.cancel_button,
															  'title': self.title, 'form_title': self.form_title, 
				   											  'form_buttom': self.form_buttom, 'sub_category': self.sub_category})