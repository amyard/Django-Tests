from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Task, Project
from django.http import HttpResponseRedirect
from .forms import *
from django.db.models import Count
from datetime import date, timedelta


User = get_user_model()


class MainClass():
	model = Project
	template_name = 'to_do/base.html'
	start_date = date.today()
	form_class  = ProjectForm
	form_class_two  = TaskForm
	button_project_title = 'Add Project'
	button_task_title = 'Add Task'
	button_action = 'Add'
	display = 'none'


class DetailMixin():
	model = None
	template_name = None
	start_date = None
	end_date = None
	form_class  = None
	form_class_two  = None
	redirect_path = None
	title = None
	detail = None
	archive = None
	button_project_title = None
	button_task_title = None
	button_action = None
	display = None


	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		user = self.request.user
		ids = self.kwargs.get('pk')

		if user:
			context['button_project_title'] = self.button_project_title
			context['button_task_title'] = self.button_task_title
			context['button_action'] = self.button_action
			context['display'] = self.display
			context['projects'] = self.model.objects.filter(user__username = user)
			context['title'] = self.title
			context['day'] = self.start_date
			context['tests'] = Project.objects.filter(user__username = user).\
										annotate(count=Count('project__title')).values('title', 'count')
			context['count_task'] = Task.objects.filter(project__user__username = user, status = 0).\
														values('project').order_by('project').annotate(count = Count('title'))
			context['uncomplited_tasks']  = Task.objects.filter(project__user__username = user, status = 0).order_by('priority')
			

			# 7 дней
			if self.end_date:
				context['dates'] = Task.objects.filter(project__user__username = user, 
												  timestamp__date__range = (self.start_date, self.end_date)).\
												  order_by('timestamp__date').values('timestamp__date').distinct()
				context['tasks'] = Task.objects.filter(project__user__username = user, status = 0,
												  timestamp__date__range = (self.start_date, self.end_date))

			# Today
			else:
				context['tasks'] = Task.objects.filter(project__user__username = user, timestamp__date = self.start_date, status = 0)

				# если на сегодня нету новых заданий, дабы отображались старые невыполненные задания
				qs = Task.objects.filter(project__user__username = user, 
												  timestamp__date = self.start_date).\
												  order_by('timestamp__date').values('timestamp__date').distinct()
				if qs:
					context['dates'] = qs
				else: 
					context['dates'] = Task.objects.filter(project__user__username = user, 
												  timestamp__date__gte =  date.today()).\
												  order_by('timestamp__date').values('timestamp__date').distinct()[:1]	


			# List View by projects - детализация по категориям
			if self.detail:
				context['uncomplited_tasks']  = None
				context['tasks'] = Task.objects.filter(project__user__username = user, status = 0,
														project_id = ids).order_by('timestamp')
				context['dates'] = Task.objects.filter(project__user__username = user, project_id = ids, status = 0).\
												  order_by('timestamp__date').values('timestamp__date').distinct()	

			# for arhive
			if self.archive:
				context['uncomplited_tasks']  = None
				context['tasks'] = Task.objects.filter(project__user__username = user,
														status = 1).order_by('timestamp')
				context['dates'] = Task.objects.filter(project__user__username = user, status = 1).\
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
				title = form.cleaned_data['title']
				color = form.cleaned_data['color']
				user = self.request.user
				project = self.model.objects.create(title = title, color = color, user = user)
				project.save()
				return HttpResponseRedirect(self.redirect_path)


		elif 'form2' in request.POST:
			form2 = self.form_class_two(request.POST or None, user = self.request.user.username)

			if form2.is_valid():
				title = form2.cleaned_data['title']
				timestamp = form2.cleaned_data['timestamp']
				project = form2.cleaned_data['project']
				priority = form2.cleaned_data['priority']
				task = Task.objects.create(title = title, timestamp = timestamp, project = project,
										   priority = priority)
				task.save()
				return HttpResponseRedirect(self.redirect_path)
		else:
			return self.form_invalid(form, form2 , **kwargs)


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