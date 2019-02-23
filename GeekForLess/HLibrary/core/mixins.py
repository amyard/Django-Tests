from datetime import date, timedelta
from .models import (Books, Genre, Location, Person, BookInfo, )
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect




##########################################################################################
#######################            LIST VIEWS FOR GENERAL PAGE      ######################
##########################################################################################


class ListMixins():
	queryset = None
	template_name = None
	title = None
	title_content = None


	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['books'] = self.queryset
		context['title'] = self.title
		context['title_content'] = self.title_content
		
		return context



##########################################################################################
#######################             DETAIL AND CREATE VIEWS         ######################
##########################################################################################


class DetailAndCreate():
	model = None
	template_name = None
	form = None
	title = None
	redirect_path = None
	form_title = None
	form_buttom = None
	paginate_by = None
	sub_category = None

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		p = Paginator(self.model.objects.select_related().all(), self.paginate_by)
		context['categories'] = p.page(context['page_obj'].number)
		context['form'] = self.form
		context['title'] = self.title
		context['form_title'] = self.form_title
		context['form_buttom'] = self.form_buttom
		context['sub_category'] = self.sub_category

		return context

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.redirect_path)

		context = {'form': form, 'categories': self.model.objects.all(), 'title': self.title, 'form_title': self.form_title, 
				   'form_buttom': self.form_buttom, 'sub_category': sub_category}
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

	def get(self, request, **kwargs):
		pk = self.kwargs.get('pk')
		categories = get_object_or_404(self.model, pk=pk)
		form = self.form(instance = categories)
		self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')

		# отображает страницу, где находится данный атрибут
		p = Paginator(self.model.objects.all(), self.paginate_by)
		if '?page=' in self.request.session['report_url']:
			num = self.request.session['report_url'].split('?page=')[-1]
			print(num)
		else:
			num = 1
		page_number = request.GET.get('page', num)
		page = p.get_page(page_number)
		return render(request, self.template_name, context = {'form': form, 'categories': page,
															  'title': self.title, 'form_title': self.form_title, 
				   											  'form_buttom': self.form_buttom, 'sub_category': self.sub_category})



	def post(self, request, **kwargs):
		pk = self.kwargs.get('pk')
		categories = get_object_or_404(self.model, pk=pk)
		form = self.form(request.POST, instance = categories)	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.request.session.get('report_url'))

		
		# отображает страницу, где находится данный атрибут
		p = Paginator(self.model.objects.all(), self.paginate_by)
		if '?page=' in self.request.META.get('HTTP_REFERER'):
			num = self.request.META.get('HTTP_REFERER').split('?page=')[-1]
			print(num)
		else:
			num = 1
		page_number = request.GET.get('page', num)
		page = p.get_page(page_number)
		return render(request, self.template_name, context = {'form': form, 'categories': page,
															  'title': self.title, 'form_title': self.form_title, 
				   											  'form_buttom': self.form_buttom, 'sub_category': self.sub_category})