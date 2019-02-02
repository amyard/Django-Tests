from datetime import date, timedelta
from .models import (Books, Genre, Location, Person, BookInfo, )
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect



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



class DetailAndCreate():
	model = None
	template_name = None
	form = None
	title = None
	redirect_path = None
	form_title = None
	form_buttom = None
	paginate_by = None

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		p = Paginator(self.model.objects.select_related().all(), self.paginate_by)
		context['categories'] = p.page(context['page_obj'].number)
		context['form'] = self.form
		context['title'] = self.title
		context['form_title'] = self.form_title
		context['form_buttom'] = self.form_buttom

		return context

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(self.redirect_path)

		context = {'form': form, 'categories': self.model.objects.all(), 'title': self.title, 'form_title': self.form_title, 
				   'form_buttom': self.form_buttom}
		return render(self.request, self.template_name, context)