from django.db import models
from django.utils import timezone
from django.urls import reverse 

# # for phone number
# from django.core.validators import RegexValidator



# Create your models here.



class Genre(models.Model):
	title = models.CharField(max_length=50)

	def __str__(self):
		return self.title



class BookManager(models.Manager):
	def all_with_prefetch_book(self):
		qs = self.get_queryset()

		return qs.prefetch_related(
					'book_information',
			)

class BookInfo(models.Model):
	title = models.CharField(max_length=120)
	author = models.CharField(max_length=150)
	published = models.CharField(max_length=4)

	genre = models.ForeignKey(Genre, on_delete = models.DO_NOTHING)

	# position here
	position = models.ForeignKey('Location', on_delete = models.CASCADE, related_name = 'position_information')
	
	objects = BookManager()

	def __str__(self):
		return self.title

	# def get_absolute_url(self):
	# 	return reverse('book_unique_detail', kwargs = {'pk':self.pk, 'title':self.title})






class LocationManager(models.Manager):
	def all_with_prefetch_location(self):
		qs = self.get_queryset()

		return qs.prefetch_related(
					'position_information',
			)

class Location(models.Model):
	room = models.PositiveIntegerField()
	bookcase = models.PositiveIntegerField()
	shelf = models.PositiveIntegerField()

	objects = LocationManager()

	def __str__(self):
		return 'Room: {}, Bookcase: {}, Shelf: {}'.format(self.room, self.bookcase, self.shelf)





class PersonManager(models.Manager):
	def all_with_prefetch_location(self):
		qs = self.get_queryset()

		return qs.prefetch_related(
					'subscriber',
			)

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




# Main model
class Books(models.Model):

	ON_HANDS = 1
	IN_LIBRARY = 0
	ALARM = -1

	STATUS = (
			(ON_HANDS, 'The book is on hands'),
			(IN_LIBRARY, 'The book is in library'),
			(ALARM, 'Need to return the book')
		)

	# need to log
	# book = models.CharField(max_length = 120)
	book = models.ForeignKey('BookInfo', on_delete = models.CASCADE, related_name = 'book_information')

	# need to log
	#person_subscription = models.CharField(max_length = 120)
	person_subscription = models.ForeignKey('Person', on_delete = models.CASCADE, related_name = 'subscriber')


	date_of_issue = models.DateField(blank= True, default=timezone.now)
	date_of_return = models.DateField(blank= True, default=timezone.now)
	status_of_book = models.IntegerField(choices = STATUS)

	def __str__(self):
		return self.book.title

	def get_absolute_url(self):
		return reverse('book_unique_detail', kwargs = {'pk':self.pk, 'title':self.book.title})
