from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Task
from django.http import HttpResponseRedirect
from .forms import *


User = get_user_model()



class DetailMixin():
	model = None
	template_name = None
	start_date = None
	end_date = None
	form_class  = None
	form_class_two  = None
	redirect_path = None
	title = None


	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		user = self.request.user

		if user:
			context['projects'] = self.model.objects.filter(user__username = user)
			context['title'] = self.title
			context['day'] = self.start_date
			context['uncomplited_tasks']  = Task.objects.filter(project__user__username = user).order_by('priority')
			if self.end_date:
				context['dates'] = Task.objects.filter(project__user__username = user, 
												  timestamp__date__range = (self.start_date, self.end_date)).\
												  order_by('timestamp__date').values('timestamp__date').distinct()
				context['tasks'] = Task.objects.filter(project__user__username = user, 
												  timestamp__date__range = (self.start_date, self.end_date))
			else:
				context['tasks'] = Task.objects.filter(project__user__username = user, timestamp__date = self.start_date)
				context['dates'] = Task.objects.filter(project__user__username = user, 
												  timestamp__date = self.start_date).\
												  order_by('timestamp__date').values('timestamp__date').distinct()
			context['form'] = self.form_class
			context['form2'] = self.form_class_two

		return context



class CreateFormMixin():

	def form_invalid(self, form, form2, **kwargs):
		return self.render_to_response(self.get_context_data({'form':form, 'form2':form2 }))


	def post(self, request, *args, **kwargs):
		form = self.form_class
		form2 = self.form_class_two

		if 'form' in request.POST:
			form = self.form_class(request.POST or None)

			if form.is_valid():
				name = form.cleaned_data['name']
				color = form.cleaned_data['color']
				user = self.request.user
				project = self.model.objects.create(name = name, color = color, user = user)
				project.save()
				return HttpResponseRedirect(self.redirect_path)


		elif 'form2' in request.POST:
			form2 = self.form_class_two(request.POST or None)

			if form2.is_valid():
				title = form2.cleaned_data['title']
				timestamp = form2.cleaned_data['timestamp']
				project = form2.cleaned_data['project']
				priority = form2.cleaned_data['priority']

				user = self.request.user
				task = Task.objects.create(title = title, timestamp = timestamp, project = project,
										   priority = priority)
				task.save()
				return HttpResponseRedirect(self.redirect_path)
		else:
			return self.form_invalid(form,form2 , **kwargs)


		context = {
			'form':form,
			'form2':form2
		}
		return render(self.request, self.redirect_path, context)



class DeleteMixin():
	model = None

	def get(self, *args, **kwargs):
		return self.post(*args, **kwargs)

	def get_success_url(self, **kwargs):
		return self.request.META.get('HTTP_REFERER')