from django import forms
from .models import City, JobDescr


class CityForm(forms.ModelForm):
	class Meta:
		model = City
		fields = ['title', 'slug', 'number_id']


class JobForm(forms.ModelForm):
	class Meta:
		model = JobDescr
		fields = ['job', 'city', 'site']
