from django import forms
from django.db.models import Q

from .models import Location, Genre, Person, BookInfo, Books


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
				'genre'
		]

	def clean(self):
		genre = self.cleaned_data['genre']
		if Genre.objects.filter(genre=genre).exists():
			raise forms.ValidationError('Such Genre exists.')



####################################################################################
####################################################################################


class PersonForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = [
				'lastname',
				'firstname',
				'birthday',
				'address',
				'phone'		
		]
		widgets = {
			'lastname': forms.TextInput(attrs={'class':'form-control'}),
			'firstname': forms.TextInput(attrs={'class':'form-control'}),
			'birthday': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),  #########
			'address': forms.TextInput(attrs={'class':'form-control'}),
			'phone': forms.TextInput(attrs={'class':'form-control'})
		}

	def clean(self):
		firstname = self.cleaned_data['firstname']
		lastname = self.cleaned_data['lastname']
		address = self.cleaned_data['address']
		phone = self.cleaned_data['phone']
		if Person.objects.filter(firstname=firstname, lastname=lastname).exists():
			raise forms.ValidationError('User with such fullname already exists.')
		if Person.objects.filter(address=address).exists():
			raise forms.ValidationError('Address is in DB')
		if Person.objects.filter(phone=phone).exists():
			raise forms.ValidationError('Such phonenumber is in DB.')


# class PersonUpdateForm(forms.ModelForm):
# 	class Meta:
# 		model = Person
# 		fields = [
# 				'lastname',
# 				'firstname',
# 				'birthday',
# 				'address',
# 				'phone'		
# 		]
# 		widgets = {
# 			'lastname': forms.TextInput(attrs={'class':'form-control'}),
# 			'firstname': forms.TextInput(attrs={'class':'form-control'}),
# 			'birthday': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),  #########
# 			'address': forms.TextInput(attrs={'class':'form-control'}),
# 			'phone': forms.TextInput(attrs={'class':'form-control'})
# 		}


####################################################################################
####################################################################################


# class BookInfoForm(forms.ModelForm):
# 	class Meta:
# 		model = BookInfo
# 		exclude = ('position',)

# 		widgets = {
# 			'title': forms.TextInput(attrs={'class':'form-control'}),
# 			'author': forms.TextInput(attrs={'class':'form-control'})
# 			}


# 	def __init__(self, *args, **kwargs):
# 		super(BookInfoForm, self).__init__(*args, **kwargs)
# 		self.fields['room']=forms.ModelChoiceField(queryset=Location.objects.values_list('room', flat=True))
# 		self.fields['bookcase']=forms.ModelChoiceField(queryset=Location.objects.values_list('bookcase', flat=True))
# 		self.fields['shelf']=forms.ModelChoiceField(queryset=Location.objects.values_list('shelf', flat=True))


class BookInfoForm(forms.ModelForm):
	class Meta:
		model = BookInfo

		fields = [
				'title',
				'author',
				'published',
				'genre',
				'position',
		]
		widgets = {
			'title': forms.TextInput(attrs={'class':'form-control'}),
			'author': forms.TextInput(attrs={'class':'form-control'})
			}

	def clean(self):
		title = self.cleaned_data['title']
		position = self.cleaned_data['position']
		if BookInfo.objects.filter(title=title).exists():
			raise forms.ValidationError('We have such book')
		if BookInfo.objects.filter(position=position).exists():
			raise forms.ValidationError('You can choose this position. There are some book')


# class BookUpdateInfoForm(forms.ModelForm):
# 	class Meta:
# 		model = BookInfo
# 		fields = [
# 				'title',
# 				'author',
# 				'published',
# 				'genre',
# 				'position'
# 		]
# 		widgets = {
# 			'title': forms.TextInput(attrs={'class':'form-control'}),
# 			'author': forms.TextInput(attrs={'class':'form-control'}),
# 			'published': forms.TextInput(attrs={'class':'form-control'})
# 			}



####################################################################################
####################################################################################



class BookForm(forms.ModelForm):
	class Meta:
		model = Books
		fields = [
				'book',
				'person_subscription',
				'date_of_issue',
				'date_of_return',
				'status_of_book'
		]
		widgets = {
			# 'title': forms.TextInput(attrs={'class':'form-control'}),
			# 'author': forms.TextInput(attrs={'class':'form-control'}),
			'date_of_issue': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
			'date_of_return': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'})
			}







# class BookInfoForm(forms.ModelForm):
# 	class Meta:
# 		model = BookInfo
# 		exclude = ('position',)

# 		widgets = {
# 			'title': forms.TextInput(attrs={'class':'form-control'}),
# 			'author': forms.TextInput(attrs={'class':'form-control'})
# 			}


# 	def __init__(self, *args, **kwargs):
# 		super(BookInfoForm, self).__init__(*args, **kwargs)
# 		self.fields['room']=forms.ModelChoiceField(queryset=Location.objects.values_list('room', flat=True))
# 		self.fields['bookcase']=forms.ModelChoiceField(queryset=Location.objects.values_list('bookcase', flat=True))
# 		self.fields['shelf']=forms.ModelChoiceField(queryset=Location.objects.values_list('shelf', flat=True))