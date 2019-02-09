from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views import View


# login and registration
from users.forms import RegistrationForms, LoginForm
from users.models import Profile
from django.contrib.auth import authenticate, login, get_user_model


# def index(request):
# 	return render(request, 'core/main.html', context = {'test':'<h1>TEST</h1>'})


class GeneralList(ListView):
	model = Profile
	template_name = 'core/main.html'

	def get_context_data(self, *args, **kwargs):
		context = super(GeneralList, self).get_context_data(*args, **kwargs)
		context['test'] = self.model.objects.all()

		return context



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
