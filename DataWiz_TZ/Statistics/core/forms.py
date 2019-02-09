from django import forms
from .models import *
from datetime import date


class SearchDateForm(forms.ModelForm):
	start_period = forms.DateField(label = 'Начальная (ближайшая) дата', 
									   widget = forms.DateInput(format = ('%Y-%m-%d'), attrs = {'type':'date'}))
	end_date = forms.DateField(label = 'Конечная дата', 
									   widget = forms.DateInput(format = ('%Y-%m-%d'), attrs = {'type':'date'}))

	class Meta:
		model = SearchDate
		fields = ['start_period', 'end_date']


	def clean(self):
		start_period = self.cleaned_data['start_period']
		end_date = self.cleaned_data['end_date']

		if start_period > date.today() or end_date > date.today():
			raise forms.ValidationError('Вы не можете использовать дату больше Сегодняшней даты.')

		if start_period == end_date:
			raise forms.ValidationError('Для корректого отобржения статистики конечная дата должна быть меньше хотя бы на один день, чем начальная дата.')

		if start_period < date.today():
			raise forms.ValidationError('Конечная дата не может быть больше Начальной (ближайшей) даты.')	
