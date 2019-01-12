# 


from django import forms

# для регистрации юзеров
from django.contrib.auth import get_user_model


class CommentForm(forms.Form):
	comment = forms.CharField(widget = forms.Textarea)
	


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)
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





# форма для регистрации форм

User = get_user_model()

class ResistrationForm(forms.ModelForm):

	# проверка пароля
	password_check = forms.CharField(widget = forms.PasswordInput)
	password = forms.CharField(widget = forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'password_check',
			'first_name',
			'last_name',
			'email'
		]


	# делаем русскоязычные название для формы
	def __init__(self, *args,**kwargs):
		super(ResistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['username'].help_text = 'Обьязательное поле'

		self.fields['password'].label = 'Пароль'
		self.fields['password_check'].label = 'Подтвердите пароль'

		self.fields['first_name'].label = 'Имя'
		self.fields['last_name'].label = 'Фамилия'
		self.fields['email'].label = 'Ваш E-mail'

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