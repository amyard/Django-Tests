from django.db import models
from django.utils import timezone
from django.urls import reverse 

# # for phone number
# from django.core.validators import RegexValidator



# Create your models here.


class Books(models.Model):

	ON_HANDS = 1
	IN_LIBRARY = 0

	STATUS = (
			(ON_HANDS, 'The book is on hands'),
			(IN_LIBRARY, 'The book is in library')
		)


	book = models.CharField(max_length = 120)
	person_subscription = models.CharField(max_length = 120)
	date_of_issue = models.DateField(blank= True, default=timezone.now)
	date_of_return = models.DateField(blank= True, default=timezone.now)
	status_of_book = models.IntegerField(choices = STATUS, default = ON_HANDS)

	def __str__(self):
		return self.book


####################################################################
####################################################################
# Main models

class Genre(models.Model):
	title = models.CharField(max_length=50)

	def __str__(self):
		return self.title



class BookInfo(models.Model):
	title = models.CharField(max_length=120)
	author = models.CharField(max_length=150)
	published = models.CharField(max_length=4)

	genre = models.ForeignKey(Genre, on_delete = models.DO_NOTHING)

	# position here
	position = models.ForeignKey('Location', on_delete = models.CASCADE, related_name = 'book_information')
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('book_unique_detail', kwargs = {'pk':self.pk, 'title':self.title})




class LocationManager(models.Manager):
	def all_with_prefetch_books(self):
		qs = self.get_queryset()

		return qs.prefetch_related(
					'book_information',
			)



class Location(models.Model):
	room = models.PositiveIntegerField()

	# стелаж
	bookcase = models.PositiveIntegerField()

	# полка
	shelf = models.PositiveIntegerField()

	objects = LocationManager()

	def __str__(self):
		return 'Room: {}, Bookcase: {}, Shelf: {}'.format(self.room, self.bookcase, self.shelf)















class Person(models.Model):

	def get_fullname(self):
		return '{} {}'.format(self.lastname, self.firstname)

	lastname = models.CharField(max_length=50)
	firstname = models.CharField(max_length=50)

	fullname = property(get_fullname)

	birthday = models.DateField(blank= True)
	address = models.TextField()

	# phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	# phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	phone = models.CharField(max_length = 20)

	def __str__(self):
		return '{} {}'.format(self.lastname, self.firstname)


