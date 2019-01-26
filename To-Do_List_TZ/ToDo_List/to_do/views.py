from django.shortcuts import render, get_object_or_404,render_to_response, reverse, redirect

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




class ProjectListView(Today, DetailMixin, CreateFormMixin, ListView):
	# model = Project
	# template_name = 'to_do/base.html'
	# start_date = date.today()
	# form_class  = ProjectForm
	# form_class_two  = TaskForm
	# redirect_path = '/'
	title = 'Today'
	redirect_path = '/'



class SevenDaysListView(DetailMixin, CreateFormMixin, ListView):
	model = Project
	template_name = 'to_do/base.html'
	start_date = date.today()+timedelta(days = 1)
	end_date = date.today()+timedelta(days = 8)
	form_class  = ProjectForm
	form_class_two  = TaskForm
	redirect_path = '/7days'
	title = '7 days'



################################################################################
########################    DELETE     #########################################
##################################################################################


class ProjectDelete(DeleteMixin, DeleteView):
	model = Project


class TaskDelete(DeleteMixin, DeleteView):
	model = Task





################################################################################
########################    CAtegory List View     ##############################
##################################################################################	


class PrjectListView(Today, DetailMixin, CreateFormMixin, ListView):
	# model = Project
	# template_name = 'to_do/base.html'
	# start_date = date.today()
	# form_class  = ProjectForm
	# form_class_two  = TaskForm
	redirect_path = '#'
	detail = True


################################################################################
########################    ARCHIVE     ##############################
##################################################################################	


class ArchiveListView(Today, DetailMixin, CreateFormMixin, ListView):
	# model = Project
	# template_name = 'to_do/base.html'
	# start_date = date.today()
	# form_class  = ProjectForm
	# form_class_two  = TaskForm
	redirect_path = '#'
	archive = True



################################################################################
########################    UPDATE     #########################################
##################################################################################	


class TodayUpdate( DetailMixin, UpdateView):

	model = Project
	template_name = 'to_do/base.html'
	start_date = date.today()
	form_class  = ProjectForm
	form_class_two  = TaskForm
	redirect_path = '/'
	title = 'Today'

# class LocationUpdateView(UpdateView):
# 	template_name = 'create.html'
# 	form_class = LocationForm
# 	queryset = Location.objects.all()
# 	success_url = '/location/'

# 	def get_object(self, *args, **kwargs):
# 		room_ = self.kwargs.get('room')
# 		bookcase_ = self.kwargs.get('bookcase')
# 		shelf_ = self.kwargs.get('shelf')

# 		return get_object_or_404(Location, room = room_, bookcase = bookcase_, shelf = shelf_)


# 	def form_valid(self, form):
# 		print(form.cleaned_data)
# 		return super(LocationUpdateView, self).form_valid(form)