# -*- coding: utf-8 -*-

from django import forms
from .models import Project, Task
from django.db.models import Q


class ProjectForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', '')
		super(ProjectForm, self).__init__(*args, **kwargs)


	title = forms.CharField(label = '', widget = forms.TextInput(attrs = { 'class':'form-control', 
		'placeholder':'Введите категорию'}))

	class Meta:
		model = Project
		fields = ['title']

	def clean(self):
		title = self.cleaned_data['title']
		if Project.objects.filter(Q(title__icontains = title.lower())&Q(user = self.user)|
			Q(title = title)&Q(user = self.user)).count():
			raise forms.ValidationError('Категория с таким именем существует.')




class TaskForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', '')
		super(TaskForm, self).__init__(*args, **kwargs)

		if self.user:
			self.fields['project'] = forms.ModelChoiceField(queryset = Project.objects.filter(user = self.user))
		self.fields['project'] = forms.ModelChoiceField(queryset=Project.objects.all())

		# try:
		# 	self.fields['project'] = forms.ModelChoiceField(queryset = Project.objects.filter(user = self.user))
		# except:
		# 	self.fields['project'] = forms.ModelChoiceField(queryset=Project.objects.all())

		self.fields['project'].label = ''
		self.fields['priority'].label = ''

	title = forms.CharField(label = '', widget = forms.TextInput(attrs = {'placeholder':'Название задания'}))
	description = forms.CharField(label = '', widget = forms.Textarea(attrs = {'placeholder':'Описание задания', 'rows':4, 'cols':150}))
	priority = forms.Select()


	class Meta:
		model = Task
		fields = ['title', 'description', 'priority', 'project']

	def clean(self):
		title = self.cleaned_data['title']
		if Task.objects.filter(Q(title__icontains = title.lower())|
			Q(title = title)|
			Q(title__iexact = title.lower())).count():
			raise forms.ValidationError('Задание с таким именем существует.')







class ProjectFormUpdate(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', '')
		super(ProjectFormUpdate, self).__init__(*args, **kwargs)


	title = forms.CharField(label = '', widget = forms.TextInput(attrs = { 'class':'form-control', 
		'placeholder':'Введите категорию'}))

	class Meta:
		model = Project
		fields = ['title']




class TaskFormUpdate(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', '')
		super(TaskFormUpdate, self).__init__(*args, **kwargs)
		try:
			self.fields['project'] = forms.ModelChoiceField(queryset = Project.objects.filter(user = self.user))
		except:
			self.fields['project'] = forms.ModelChoiceField(queryset = Project.objects.all())
		self.fields['project'].label = ''
		self.fields['priority'].label = ''

	title = forms.CharField(label = '', widget = forms.TextInput(attrs = {'placeholder':'Название задания'}))
	description = forms.CharField(label = '', widget = forms.Textarea(attrs = {'placeholder':'Описание задания', 'rows':4, 'cols':150}))
	priority = forms.Select()


	class Meta:
		model = Task
		fields = ['title', 'description', 'priority', 'project']