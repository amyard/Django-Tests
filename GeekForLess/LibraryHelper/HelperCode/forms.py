from django import forms

from .models import Location, Genre


class LocationForm(forms.ModelForm):
	class Meta:
		model = Location
		fields = [
				'room',
				'bookcase',
				'shelf'
		]
		widgets = {
			'room': forms.TextInput(attrs={'class':'form-control'}),
			'bookcase': forms.TextInput(attrs={'class':'form-control'}),
			'shelf': forms.TextInput(attrs={'class':'form-control'})
		}








class GenreForm(forms.ModelForm):
	class Meta:
		model = Genre
		fields = [
				'title'
		]
		widgets = {
			'title': forms.TextInput()
		}