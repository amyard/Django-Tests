from django.views.generic.list import MultipleObjectMixin
from django.core.paginator import Paginator
from .forms import *
from django.db.models import Count
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect


class DeleteMixin(MultipleObjectMixin):
	model = None

	def get(self, *args, **kwargs):
		return self.post(*args, **kwargs)

	def get_success_url(self, **kwargs):
		return self.request.META.get('HTTP_REFERER')







class CreateMixin(MultipleObjectMixin):
	model = None
	model2 = None
	template_name = None
	title = None
	paginate_by = None
	form = None
	form2 = None
	redirect_path = None


	def get_queryset(self):
		return self.model2.objects.filter(project__user__username = self.request.user)


	def get(self, request, **kwargs):
		user = self.request.user
		projects = self.model.objects.filter(user__username = user)
		df = self.get_queryset()
	
		p = Paginator(df, self.paginate_by)
		page_number = request.GET.get('page')
		page = p.get_page(page_number)

		title = self.title

		if self.request.user.is_anonymous:
			form2 = self.form2()
		else:
			form2 = self.form2(user=self.request.user)
		form = self.form

		count_tasks = self.model.objects.filter(user__username = user).annotate(count=Count('project__title')).values('title', 'count')
		self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
		context = {'projects':projects, 'tasks':page, 'title':title, 'form':form, 'form2':form2, 'count_tasks':count_tasks}

		return render(request, self.template_name, context)


	def form_invalid(self, form, form2, **kwargs):
		return self.render_to_response(self.get({'form':form, 'form2':form2 }))


	def post(self, request, **kwargs):
		form = self.form
		form2 = self.form2(user = self.request.user)

		if 'form2' in request.POST:
			form2 = self.form2(request.POST or None, user = self.request.user)
			if form2.is_valid():
				form2.save()
				return HttpResponseRedirect(self.request.session.get('report_url'))

			else:
				print(form2.errors)
		elif 'form' in request.POST:
			form = self.form(request.POST or None, user = self.request.user)
			if form.is_valid():
				form = form.save(commit = False)
				form.user = request.user
				form.save()
				return HttpResponseRedirect(self.request.session.get('report_url'))
		else:
			return render(self.request, self.template_name, {'form2':form2, 'form':form})

		user = self.request.user
		projects = self.model.objects.filter(user__username = user)
		df = self.get_queryset()
	
		p = Paginator(df, self.paginate_by)
		page_number = request.GET.get('page')
		page = p.get_page(page_number)

		title = self.title
		count_tasks = self.model.objects.filter(user__username = user).annotate(count=Count('project__title')).values('title', 'count')


		context = {'form2':form2, 'form':form, 'tasks':page, 'projects':projects, 'title':title, 'count_tasks':count_tasks}

		return render(self.request, self.template_name, context)
