from django import forms
from django.db.models import Q

from .models import Location, Genre, Person, BookInfo, Books


class LocationForm(forms.ModelForm):
	class Meta:
		model = Location
		fields = ['room', 'bookcase', 'shelf']

		widgets = {
			'room': forms.TextInput(attrs={'class':'form-control'}),
			'bookcase': forms.TextInput(attrs={'class':'form-control'}),
			'shelf': forms.TextInput(attrs={'class':'form-control'})
		}




####################################################################################
####################################################################################


class GenreForm(forms.ModelForm):
	class Meta:
		model = Genre
		fields = ['genre']


	def clean(self):
		genre = self.cleaned_data['genre']
		if Genre.objects.filter(genre=genre).exists():
			raise forms.ValidationError('Such Genre exists.')



####################################################################################
####################################################################################


class PersonForm(forms.ModelForm):
	class Meta:
		model = Person
		fields = ['lastname', 'firstname', 'birthday', 'address', 'phone']
		widgets = {
			'lastname': forms.TextInput(attrs={'class':'form-control'}),
			'firstname': forms.TextInput(attrs={'class':'form-control'}),
			'birthday': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),  #########
			'address': forms.TextInput(attrs={'class':'form-control'}),
			'phone': forms.TextInput(attrs={'class':'form-control'})
		}


####################################################################################
####################################################################################


class BookInfoForm(forms.ModelForm):
	class Meta:
		model = BookInfo

		fields = ['title','author','published','genre','position']
		widgets = {
			'title': forms.TextInput(attrs={'class':'form-control'}),
			'author': forms.TextInput(attrs={'class':'form-control'})
			}

####################################################################################
####################################################################################



class BookForm(forms.ModelForm):
	class Meta:
		model = Books
		fields = ['book','person_subscription','date_of_issue','date_of_return','status_of_book']
		widgets = {
			'date_of_issue': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
			'date_of_return': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'})
			}



#######################################################################################################
########################         попробовать локации переделать             ###########################
#######################################################################################################
########################         или FORMSET             ###########################
#######################################################################################################



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