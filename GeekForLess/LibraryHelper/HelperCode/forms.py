from django import forms
from django.db.models import Q

from .models import Location, Genre, Person


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

	def clean(self):
		room = self.cleaned_data['room']
		bookcase = self.cleaned_data['bookcase']
		shelf = self.cleaned_data['shelf']
		if Location.objects.filter(room=room, bookcase=bookcase, shelf=shelf).exists():
			raise forms.ValidationError('Such Position in library already in use.')




####################################################################################
####################################################################################


class GenreForm(forms.ModelForm):
	class Meta:
		model = Genre
		fields = [
				'title'
		]
		# widgets = {
		# 	'title': forms.CharField(is_hidden = False)
		# }


	def clean(self):
		title = self.cleaned_data['title']
		if Genre.objects.filter(title=title).exists():
			raise forms.ValidationError('Such Genre exists.')



####################################################################################
####################################################################################


class PersonForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = [
				'lastname',
				'firstname',
				'birthday',  # datefield
				'address',
				'phone'		
		]
		widgets = {
			'lastname': forms.TextInput(attrs={'class':'form-control'}),
			'firstname': forms.TextInput(attrs={'class':'form-control'}),
			'birthday': forms.TextInput(attrs={'class':'form-control'}),  #########
			'address': forms.TextInput(attrs={'class':'form-control'}),
			'phone': forms.TextInput(attrs={'class':'form-control'})
		}

	def clean(self):
		firstname = self.cleaned_data['firstname']
		lastname = self.cleaned_data['lastname']
		address = self.cleaned_data['address']
		phone = self.cleaned_data['phone']
		if Person.objects.filter(firstname=firstname, lastname=name).exists():
			raise forms.ValidationError('User with such fullname already exists.')
		if Person.objects.filter(address=address).exists():
			raise forms.ValidationError('Address is in DB')
		if Person.objects.filter(phone=phone).exists():
			raise forms.ValidationError('Such phonenumber is in DB.')