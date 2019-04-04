from django import forms
from .models import Project, Task
from django.core.exceptions import ValidationError



class ProjectForm(forms.ModelForm):


	title = forms.CharField(label = '', widget = forms.TextInput(attrs = { 'class':'form-control', 
																'placeholder':'Type Project',
																}))
	color = forms.CharField(label = '', widget = forms.TextInput(attrs = {'class':'form-control', 
																'placeholder':'Color'}))

	class Meta:
		model = Project
		fields = ['title', 'color']

	# def clean(self):
	# 	name = self.cleaned_data['name'].lower()
	# 	color = self.cleaned_data['color'].lower()

		# if Project.objects.filter(name__iexact = name).count():
		# 	raise ValidationError("Projects's name already in use.")
		# if Project.objects.filter(name__iexact = color).count():
		# 	raise ValidationError("You can not use this color again.")







class TaskForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user','')
		super(TaskForm, self).__init__(*args, **kwargs)

		self.fields['project'] = forms.ModelChoiceField(queryset=Project.objects.filter(user__username = user))

		self.fields['project'].label = ''
		self.fields['priority'].label = ''
		



	title = forms.CharField(label = '', widget = forms.TextInput(attrs = {
																'placeholder':'Task name'}))
	timestamp = forms.DateTimeField(label = '', widget = forms.DateInput(format=('%Y-%m-%d'), 
												attrs = { 'type':'date'}))

	# project = forms.Select()
	# project = forms.ModelChoiceField(queryset=Project.objects.filter(user = user))
	# project = forms.ModelChoiceField(queryset=Project.objects.all())
	priority = forms.Select()

	class Meta:
		model = Task
		fields = ['title', 'timestamp', 'project', 'priority']



	