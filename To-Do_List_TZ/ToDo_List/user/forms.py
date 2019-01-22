from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()



class LoginForm(forms.Form):
	username = forms.CharField(widget = forms.TextInput(attrs = {'class':'form-control'}))
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control'}))

	def __init__(self, *args,**kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'


	def clean(self):
		# проверяем уникальность имени пользователя
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		
		if not User.objects.filter(username = username).exists():
			raise forms.ValidationError('Не существует такого пользователя')

		user = User.objects.get(username=username)
		if not user.check_password(password):
			raise forms.ValidationError('Неверный пароль')


class RegistrationForm(forms.ModelForm):

	# проверка пароля
	password_check = forms.CharField(widget = forms.PasswordInput())
	password = forms.CharField(widget = forms.PasswordInput())

	class Meta:
		model = User
		fields = ['username', 'password', 'password_check']

	# делаем русскоязычые названия для формы
	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['username'].help_text = 'Обьязательное поле'

		self.fields['password'].label = 'Пароль'
		self.fields['password'].help_text = 'Обьязательное поле'
		self.fields['password_check'].label = 'Подтвердите пароль'
		self.fields['password_check'].help_text = 'Обьязательное поле'


	# обработчик ошибок
	def clean(self):
		# проверяем уникальность имени пользователя
		username = self.cleaned_data['username']
		if User.objects.filter(username = username).exists():
			raise forms.ValidationError('Пользователь с таким именем уже существует')

		# проверка пароля
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']
		if password != password_check:
			raise forms.ValidationError('Ваши пароли не совпадают')
