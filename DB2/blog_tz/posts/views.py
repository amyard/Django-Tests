from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect


from users.models import Subscriber
from users.forms import RegistrationForm, LoginForm
from django.views import View
from django.contrib.auth import authenticate, login, get_user_model

from django.contrib import messages


def MainTestView(request):
	try:
		profile = Subscriber.objects.get(user = request.user)
		return render(request, 'posts/main.html', {'info': 'We have all info about user right now', 'user': request.user, 'profile':profile})
	except:
		return render(request, 'posts/main.html', {'info':'We have all info about user right now', 'user': request.user})
