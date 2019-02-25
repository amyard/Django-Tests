from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Project

from user.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, get_user_model
from django.views import View
from user.models import UserAccount


#########################################################################################
##################################        USERS       ###################################
#########################################################################################

User = get_user_model()

class LoginView(View):
	template_name = 'users/login.html'
	form = LoginForm

	def get(self, request, *args, **kwargs):
		form = self.form
		context = {'form': form}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username = username, password = password)
			if user:
				login(self.request, user)
			return HttpResponseRedirect('/')
		context = {'form': form}
		return render(self.request, self.template_name, context)



class RegistrationView(View):
	template_name = 'users/registration.html'
	form = RegistrationForm

	def get(self, request,*args,**kwargs):
		form = self.form
		context = {'form':form}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			new_user = form.save(commit = False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			new_user.set_password(password)
			password_check = form.cleaned_data['password_check']
			new_user.save()
			UserAccount.objects.create(user = User.objects.get(username=new_user.username))
			return HttpResponseRedirect('../login')
		context = {'form':form}
		return render(self.request, self.template_name, context)















class CategoryListView(ListView):
	model = Project
	template_name = 'core/main.html'
	title = 'Main page'

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryListView, self).get_context_data(*args, **kwargs)
		user = self.request.user

		context['projects'] = self.model.objects.filter(user__username = user)
		context['title'] = self.title
		return context
