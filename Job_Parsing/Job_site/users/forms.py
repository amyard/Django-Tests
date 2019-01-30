from django import forms
from .models import Subscriber
from django.contrib.auth.models import User
import re
from django.core.validators import validate_email 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')




class RegistrationForm(forms.ModelForm):

	email = forms.CharField(widget = forms.EmailInput())
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control'}))
	password_check = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control'}))

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'password_check']

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['email'].label = 'Электронная почта'
		self.fields['password'].label = 'Пароль'
		self.fields['password_check'].label = 'Подтвердите пароль'

		self.fields['username'].help_text = 'Обьязательное поле' 
		self.fields['email'].help_text = 'Обьязательное поле'
		self.fields['password'].help_text = 'Обьязательное поле' 
		self.fields['password_check'].help_text = 'Обьязательное поле'


	def clean(self):
		username = self.cleaned_data['username']
		email = self.cleaned_data['email']
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']



		if '@' not in email:
			raise forms.ValidationError('Отсутствие @ в электронной почте.')

		if '.' not in email:
			raise forms.ValidationError('Отсутствие . в электронной почте.')

		if User.objects.filter(username = username).exists():
			raise forms.ValidationError('Пользователь с таким именем уже существует')

		if User.objects.filter(email = email).exists():
			raise forms.ValidationError('Не лзя использовать данную электронную почту.')

		if password != password_check:
			raise forms.ValidationError('Ваши пароли не совпали')

		# if not EMAIL_REGEX.match(email):
		# 	raise forms.ValidationError('Не правильная электронная почта')

		try: 
			mt =  validate_email(email)
		except:
			raise forms.ValidationError('Не правильная электронная почта')





class LoginForm(forms.Form):

	username = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control'}))

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		
		if not User.objects.filter(username = username).exists():
			raise forms.ValidationError('Не существует такого пользователя')

		user = User.objects.get(username=username)
		if not user.check_password(password):
			raise forms.ValidationError('Неверный пароль')