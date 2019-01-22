from django.shortcuts import render, get_object_or_404

from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, get_user_model

from user.models import UserAccount
from .models import Project

from user.forms import LoginForm, RegistrationForm

from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView,)
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q




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


class ProjectListView(ListView):
	model = Project
	template_name = 'to_do/base.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ProjectListView, self).get_context_data(*args, **kwargs)
		user = self.request.user

		if user:
			context['projects'] = self.model.objects.filter(user__username = user)
		# else:
		# 	context['projects'] = self.model.objects.all()


		return context

