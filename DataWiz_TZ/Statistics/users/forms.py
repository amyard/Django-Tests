from django import forms
from django.contrib.auth import get_user_model




User = get_user_model()



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

		user = User.objects.get(username = username)
		if not user.check_password(password):
			raise forms.ValidationError('Неверный пароль')





class RegistrationForms(forms.ModelForm):

	username = forms.CharField(widget = forms.TextInput())
	password = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control'}))
	password_check = forms.CharField(widget = forms.PasswordInput(attrs = {'class':'form-control'}))

	class Meta:
		model = User
		fields = ['username', 'password', 'password_check']

	def __init__(self, *args, **kwargs):
		super(RegistrationForms, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'
		self.fields['password_check'].label = 'Подтвердите пароль'

		self.fields['username'].help_text = 'Обьязательное поле'
		self.fields['password'].help_text = 'Обьязательное поле'
		self.fields['password_check'].help_text = 'Обьязательное поле'

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']

		if User.objects.filter(username = username).exists():
			raise forms.ValidationError('Пользователь с таким именем уже существует')

		if '@' not in username:
			raise forms.ValidationError('Отсутствие @ в имени Логина.')

		if '.' not in username:
			raise forms.ValidationError('Отсутствие . в имени Логина.')

		if password != password_check:
			raise forms.ValidationError('Ваши пароли не совпадают')



	
