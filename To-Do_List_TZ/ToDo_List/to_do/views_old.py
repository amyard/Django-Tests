from django.shortcuts import render, get_object_or_404,render_to_response

from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, get_user_model

from user.models import UserAccount
from .models import Project, Task

from user.forms import LoginForm, RegistrationForm

from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q
from datetime import date, timedelta

# forms
from django.views.generic.edit import FormMixin
from .forms import ProjectForm, TaskForm

from .mixins import *


#########################################################################################
##################################        USERS       ###################################
#########################################################################################

User = get_user_model()



class LoginView(View):
	template_name = 'users/login.html'

	def get(self,request,*args,**kwargs):
		form = LoginForm()
		context = {
				'form':form
		}

		return render(self.request, self.template_name, context)


	def post(self, request, *args,**kwargs):
		form = LoginForm(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user:
				login(self.request, user)
			
			return HttpResponseRedirect('/')
		context = {
				'form':form
		}

		return render(self.request, self.template_name, context)




class RegistrationView(View):
	template_name = 'users/registration.html'

	def get(self, request,*args,**kwargs):
		form = RegistrationForm()
		context = {
				'form':form
		}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = RegistrationForm(request.POST or None)
		if form.is_valid():
			new_user = form.save(commit = False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			new_user.set_password(password)
			password_check = form.cleaned_data['password_check']
			new_user.save()
			UserAccount.objects.create(user = User.objects.get(username=new_user.username))
			return HttpResponseRedirect('../login')
		context = {
			'form':form
		}
		return render(self.request, self.template_name, context)







#########################################################################################
##################################        TO-DO       ###################################
#########################################################################################


# Create your views here.
def home(request):
	return render(request, 'to_do/base.html')

# class ProjectListView(ListView):
# 	model = Project
# 	template_name = 'to_do/base.html'
# 	start_date = date.today()
# 	form_class  = ProjectForm
# 	form_class_two  = TaskForm


# 	def get_context_data(self, *args, **kwargs):
# 		context = super(ProjectListView, self).get_context_data(*args, **kwargs)
# 		user = self.request.user

# 		if user:
# 			context['projects'] = self.model.objects.filter(user__username = user)
# 			context['tasks'] = Task.objects.filter(project__user__username = user, timestamp__date = self.start_date)
# 			context['title'] = 'Today'
# 			context['day'] = self.start_date
# 			context['form'] = self.form_class
# 			context['form2'] = TaskForm
# 		return context


	# Project
	# def post(self, request, *args, **kwargs):
	# 	form = ProjectForm(request.POST or None)
	# 	if form.is_valid():
	# 		title = form.cleaned_data['title']
	# 		color = form.cleaned_data['color']
	# 		user = self.request.user
	# 		project = Project.objects.create(title = title, color = color, user = user)
	# 		project.save()
	# 		return HttpResponseRedirect('/')
	# 	context = {
	# 		'form':form
	# 	}
	# 	return render(self.request, self.template_name, context)


	# TASK
	# def post(self, request, *args, **kwargs):
	# 	form = TaskForm(request.POST or None)
	# 	if form.is_valid():
	# 		title = form.cleaned_data['title']
	# 		timestamp = form.cleaned_data['timestamp']
	# 		project = form.cleaned_data['project']
	# 		priority = form.cleaned_data['priority']

	# 		user = self.request.user
	# 		task = Task.objects.create(title = title, timestamp = timestamp, project = project,
	# 								   priority = priority)
	# 		task.save()
	# 		return HttpResponseRedirect('/')
	# 	context = {
	# 		'form':form
	# 	}
	# 	return render(self.request, self.template_name, context)







# class SevenDaysListView(ListView):
# 	model = Project
# 	template_name = 'to_do/base.html'
# 	start_date = date.today()+timedelta(days = 1)
# 	end_date = date.today()+timedelta(days = 8)
# 	form_class  = ProjectForm
# 	form_class_two  = TaskForm

# 	def get_context_data(self, *args, **kwargs):
# 		context = super(SevenDaysListView, self).get_context_data(*args, **kwargs)
# 		user = self.request.user

# 		if user:
# 			context['projects'] = self.model.objects.filter(user__username = user)
# 			context['tasks'] = Task.objects.filter(project__user__username = user, 
# 												  timestamp__date__range = (self.start_date, self.end_date))
# 			context['title'] = '7 days'
# 			context['day'] = self.start_date
# 			context['dates'] = Task.objects.filter(project__user__username = user, 
# 												  timestamp__date__range = (self.start_date, self.end_date)).\
# 												  order_by('timestamp__date').values('timestamp__date').distinct()
# 			context['form'] = self.form_class
# 			context['form2'] = self.form_class_two

# 		return context

# 	def form_invalid(self, form, form2, **kwargs):
# 		return self.render_to_response(self.get_context_data({'form':form, 'form2':form2 }))


# 	def post(self, request, *args, **kwargs):
# 		form = ProjectForm()
# 		form2 = TaskForm()

# 		if 'form' in request.POST:
# 			form = ProjectForm(request.POST or None)

# 			if form.is_valid():
# 				title = form.cleaned_data['title']
# 				color = form.cleaned_data['color']
# 				user = self.request.user
# 				project = Project.objects.create(title = title, color = color, user = user)
# 				project.save()
# 				return HttpResponseRedirect('/7days')


# 		elif 'form2' in request.POST:
# 			form2 = TaskForm(request.POST or None)

# 			if form2.is_valid():
# 				title = form2.cleaned_data['title']
# 				timestamp = form2.cleaned_data['timestamp']
# 				project = form2.cleaned_data['project']
# 				priority = form2.cleaned_data['priority']

# 				user = self.request.user
# 				task = Task.objects.create(title = title, timestamp = timestamp, project = project,
# 										   priority = priority)
# 				task.save()
# 				return HttpResponseRedirect('/7days')
# 		else:
# 			return self.form_invalid(form,form2 , **kwargs)


# 		context = {
# 			'form':form,
# 			'form2':form2
# 		}
# 		return render(self.request, '/7days', context)



################################################################################
################################################################################
##################################################################################


class ProjectListView(ListView):
	model = Project
	template_name = 'to_do/base.html'
	start_date = date.today()
	form_class  = ProjectForm
	form_class_two  = TaskForm


	def get_context_data(self, *args, **kwargs):
		context = super(ProjectListView, self).get_context_data(*args, **kwargs)
		user = self.request.user

		if user:
			context['projects'] = self.model.objects.filter(user__username = user)
			context['tasks'] = Task.objects.filter(project__user__username = user, timestamp__date = self.start_date)
			context['title'] = 'Today'
			context['day'] = self.start_date
			context['form'] = self.form_class
			context['form2'] = self.form_class_two
		return context
	

	def form_invalid(self, form, form2, **kwargs):
		return self.render_to_response(self.get_context_data({'form':form, 'form2':form2 }))



	def post(self, request, *args, **kwargs):
		form = ProjectForm()
		form2 = TaskForm()

		if 'form' in request.POST:
			form = ProjectForm(request.POST or None)

			if form.is_valid():
				title = form.cleaned_data['title']
				color = form.cleaned_data['color']
				user = self.request.user
				project = Project.objects.create(title = title, color = color, user = user)
				project.save()
				return HttpResponseRedirect('/')


		elif 'form2' in request.POST:
			form2 = TaskForm(request.POST or None)

			if form2.is_valid():
				title = form2.cleaned_data['title']
				timestamp = form2.cleaned_data['timestamp']
				project = form2.cleaned_data['project']
				priority = form2.cleaned_data['priority']

				user = self.request.user
				task = Task.objects.create(title = title, timestamp = timestamp, project = project,
										   priority = priority)
				task.save()
				return HttpResponseRedirect('/')
		else:
			return self.form_invalid(form,form2 , **kwargs)


		context = {
			'form':form,
			'form2':form2
		}
		return render(self.request, self.template_name, context)



#########################################################################################
##################################        Test       ###################################
#########################################################################################



class SevenDaysListView(DetailMixin, CreateFormMixin, ListView):
	model = Project
	template_name = 'to_do/base.html'
	start_date = date.today()+timedelta(days = 1)
	end_date = date.today()+timedelta(days = 8)
	form_class  = ProjectForm
	form_class_two  = TaskForm
	redirect_path = '/7days'

	# def get_context_data(self, *args, **kwargs):
	# 	context = super(SevenDaysListView, self).get_context_data(*args, **kwargs)
	# 	user = self.request.user

	# 	if user:
	# 		context['projects'] = self.model.objects.filter(user__username = user)
	# 		context['tasks'] = Task.objects.filter(project__user__username = user, 
	# 											  timestamp__date__range = (self.start_date, self.end_date))
	# 		context['title'] = '7 days'
	# 		context['day'] = self.start_date
	# 		context['dates'] = Task.objects.filter(project__user__username = user, 
	# 											  timestamp__date__range = (self.start_date, self.end_date)).\
	# 											  order_by('timestamp__date').values('timestamp__date').distinct()
	# 		context['form'] = self.form_class
	# 		context['form2'] = self.form_class_two

	# 	return context

	# def form_invalid(self, form, form2, **kwargs):
	# 	return self.render_to_response(self.get_context_data({'form':form, 'form2':form2 }))


	# def post(self, request, *args, **kwargs):
	# 	form = ProjectForm()
	# 	form2 = TaskForm()

	# 	if 'form' in request.POST:
	# 		form = ProjectForm(request.POST or None)

	# 		if form.is_valid():
	# 			title = form.cleaned_data['title']
	# 			color = form.cleaned_data['color']
	# 			user = self.request.user
	# 			project = Project.objects.create(title = title, color = color, user = user)
	# 			project.save()
	# 			return HttpResponseRedirect('/7days')


	# 	elif 'form2' in request.POST:
	# 		form2 = TaskForm(request.POST or None)

	# 		if form2.is_valid():
	# 			title = form2.cleaned_data['title']
	# 			timestamp = form2.cleaned_data['timestamp']
	# 			project = form2.cleaned_data['project']
	# 			priority = form2.cleaned_data['priority']

	# 			user = self.request.user
	# 			task = Task.objects.create(title = title, timestamp = timestamp, project = project,
	# 									   priority = priority)
	# 			task.save()
	# 			return HttpResponseRedirect('/7days')
	# 	else:
	# 		return self.form_invalid(form,form2 , **kwargs)


	# 	context = {
	# 		'form':form,
	# 		'form2':form2
	# 	}
	# 	return render(self.request, '/7days', context)



################################################################################
########################    UPDATE     #########################################
##################################################################################	


class ProjectUpdate(View):
	model = Project
	template_name = 'to_do/base.html'
	start_date = date.today()
	form_class  = ProjectForm
	form_class_two  = TaskForm
	redirect_path = '/'
	title = 'Today'
	queryset = Project.objects.all()
	button_project_title = 'Edit Project'
	button_task_title = 'Edit Task'
	button_action = 'Edit'
	display_js = 'block'


	def get(self, request, **kwargs):
		pk = self.kwargs.get('pk')
		user = self.request.user
		tag = Project.objects.get(id = pk)
		form = ProjectForm(instance = tag)
		form2 = TaskForm
		self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
		return render(request, 'to_do/base.html', context = {'form':form, 
															 'form2':form2,
															 'button_project_title': self.button_project_title,
															 'button_task_title': self.button_task_title,
															 'button_action':self.button_action,
															 'display': self.display_js,
															 'uncomplited_tasks': None,
															 'tasks': Task.objects.filter(project__user__username = user, timestamp__gte = date.today()).order_by('timestamp'),
															 'dates': Task.objects.filter(project__user__username = user, timestamp__gte = date.today()).order_by('timestamp__date').values('timestamp__date').distinct(),
															 'projects': self.model.objects.filter(user__username = user),
															 'count_task': Task.objects.filter(project__user__username = user, status = 0).values('project').order_by('project').annotate(count = Count('title'))
															  })



	def post(self, request, **kwargs):
		pk = self.kwargs.get('pk')
		tag = Project.objects.get(id = pk)
		form = ProjectForm(request.POST, instance = tag)
		form2 = TaskForm

		if form.is_valid():
			new_tag = form.save()
			return HttpResponseRedirect(self.request.session.get('report_url'))
		return render(request, self.template_name, context = {'form':form, 'form2':form2})


class TaskUpdate(View):
	model = Project
	template_name = 'to_do/base.html'
	start_date = date.today()
	form_class  = ProjectForm
	form_class_two  = TaskForm
	redirect_path = '/'
	title = 'Today'
	queryset = Project.objects.all()
	button_project_title = 'Edit Project'
	button_task_title = 'Edit Task'
	button_action = 'Edit'
	display_js = 'block'


	def get(self, request, **kwargs):
		pk = self.kwargs.get('pk')
		user = self.request.user
		tag = Task.objects.get(id = pk)
		form = ProjectForm
		form2 = TaskForm(instance = tag)
		self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
		return render(request, 'to_do/base.html', context = {'form':form, 
															 'form2':form2,
															 'title': 'Detail',
															 'button_project_title': self.button_project_title,
															 'button_task_title': self.button_task_title,
															 'button_action':self.button_action,
															 'display': self.display_js,
															 'uncomplited_tasks': None,
															 'tasks': Task.objects.filter(project__user__username = user, timestamp__gte = date.today()).order_by('timestamp'),
															 'dates': Task.objects.filter(project__user__username = user, timestamp__gte = date.today()).order_by('timestamp__date').values('timestamp__date').distinct(),
															 'projects': self.model.objects.filter(user__username = user),
															 'count_task': Task.objects.filter(project__user__username = user, status = 0).values('project').order_by('project').annotate(count = Count('title'))
															  })



	def post(self, request, **kwargs):
		pk = self.kwargs.get('pk')
		tag = Task.objects.get(id = pk)
		form = ProjectForm
		form2 = TaskForm(request.POST, instance = tag)

		if form2.is_valid():
			new_tag = form2.save()
			return HttpResponseRedirect(self.request.session.get('report_url'))
		return render(request, self.template_name, context = {'form':form, 'form2':form2})



################################################################################
########################    Done     #########################################
##################################################################################


class DoneView(View):
	model = Task
	template_name = 'to_do/base.html'


	def get(self, reguest, **kwargs):
		pk = self.kwargs.get('pk')
		self.model.objects.filter(id = pk)
		self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
		return render(request, self.request.session['report_url'])

	def get(self, reguest, **kwargs):
		pk = self.kwargs.get('pk')
		self.model.objects.filter(id = pk).update(status = 1)
		self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
		return HttpResponseRedirect(self.request.session['report_url'])