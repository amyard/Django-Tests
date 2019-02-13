from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views import View

from .forms import SearchDateForm

from core.script_API.script import main_script


# login and registration
from users.forms import RegistrationForms, LoginForm
from users.models import Profile
from django.contrib.auth import authenticate, login, get_user_model


# def index(request):
# 	return render(request, 'core/main.html', context = {'test':'<h1>TEST</h1>'})




#####################################################################################
######################################     LOGIN     ################################
#####################################################################################
User = get_user_model()


class LoginView(View):
	template_name = 'users/login.html'
	form = LoginForm
	title = 'Вход'
	content_title = 'Авторизация пользователя:'
	btn = 'Войти'

	def get(self, request, *args, **kwargs):
		form = self.form
		context = {'form':form, 'title':self.title, 'content_title':self.content_title, 'btn':self.btn}
		return render(request, self.template_name, context = context)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			sub = authenticate(username = username, password = password)
			if sub:
				login(self.request, sub)
			return HttpResponseRedirect('/')
		context = {'form':form, 'title':self.title, 'content_title':self.content_title, 'btn':self.btn}
		return render(self.request, self.template_name, context = context)



#####################################################################################
######################################  REGISTRATION  ###############################
#####################################################################################

class RegistrationView(View):
	template_name = 'users/login.html'
	form = RegistrationForms
	title = 'Регистрация'
	content_title = 'Регистрация:'
	btn = 'Зарегестрировать'

	def get(self, *args, **kwargs):
		form = self.form
		context = {'form':form, 'title':self.title, 'content_title':self.content_title, 'btn':self.btn}
		return render(self.request, self.template_name, context = context)		

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			new_user = form.save(commit = False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			new_user.set_password(password)
			username = form.cleaned_data['username']
			new_user.save()
			Profile.objects.create(user = User.objects.get(username = new_user.username))
			return HttpResponseRedirect('../login')
		context = {'form':form, 'title':self.title, 'content_title':self.content_title, 'btn':self.btn}
		return render(self.request, self.template_name, context = context)	


#####################################################################################
######################################  LIST VIEW    ################################
#####################################################################################


class GeneralList(View):
	model = Profile
	template_name = 'core/main.html'
	form = SearchDateForm


	def get(self, request, **kwargs):
		form = self.form
		context = {'form':form, 'test': self.model.objects.all()}	
		return render(self.request, self.template_name, context = context)


	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		user = self.request.user
		if form.is_valid():



			start_period = form.cleaned_data['start_period']
			end_date = form.cleaned_data['end_date']

			if user.is_authenticated and not user.is_superuser:

				password = Profile.objects.values_list('password', flat=True).get(user__username = user.username)

				dfs, pos, neg, uniq_date = main_script(date_from=start_period, date_to=end_date, log = user.username, pas = password)
			else:
				dfs, pos, neg, uniq_date = main_script(date_from=start_period, date_to=end_date)

			return render(self.request, self.template_name, context = {'form':form, 'dfs': dfs, 'pos':pos, 'neg':neg, 'uniq_date':uniq_date})
			
		context = {'form':form, 'test': self.model.objects.all()}	
		return render(self.request, self.template_name, context = context)