from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect


from users.models import Subscriber
from users.forms import RegistrationForm, LoginForm
from django.views import View
from django.contrib.auth import authenticate, login, get_user_model

from django.contrib import messages


def MainTestView(request):
	return render(request, 'posts/main.html', {'info':'New redirect info is here', 'user': request.user})


User = get_user_model()


class RegistrationView(View):
	template_name = 'users/registration.html'
	form = RegistrationForm
	message_send = 'You have registered account.'

	def get(self, request, *args, **kwargs):
		form = self.form
		context = {'form': form}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			new_user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			new_user.set_password(password)
			password_check = form.cleaned_data['password_check']
			new_user.save()
			Subscriber.objects.create(user=User.objects.get(username=new_user.username))

			messages.success(self.request, self.message_send)

			return HttpResponseRedirect('../login')
		context = {'form': form}
		return render(self.request, self.template_name, context)



class LoginView(View):
	template_name = 'users/login.html'
	form = LoginForm
	message_send = 'You are logged in.'

	def get(self, request, *args, **kwargs):
		form = self.form
		context = {'form': form}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			log_user = User.objects.get(email = email)

			user = authenticate(username = log_user.username, password = password)
			if user:
				login(self.request, user)
				messages.success(self.request, self.message_send)
			return HttpResponseRedirect('/')
		context = {'form': form}
		return render(self.request, self.template_name, context)