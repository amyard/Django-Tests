from django.db import models
from django.utils import timezone
from django.urls import reverse 

from datetime import date, timedelta





# Create your models here.
class Genre(models.Model):
	genre = models.CharField(max_length=50, unique = True)

	def __str__(self):
		return self.genre

	class Meta:
		ordering = ['id']


class Location(models.Model):
	room = models.PositiveIntegerField()
	bookcase = models.PositiveIntegerField()
	shelf = models.PositiveIntegerField()


	def __str__(self):
		return f'Room: {self.room}, Bookcase: {self.bookcase}, Shelf: {self.shelf}'
	
	class Meta:
		ordering = ['room','bookcase','shelf']


class BookInfo(models.Model):
	title = models.CharField(max_length=120)
	author = models.CharField(max_length=150)
	published = models.CharField(max_length=4)

	genre = models.ForeignKey(Genre, on_delete = models.DO_NOTHING, related_name = 'genre_info')

	# position here
	position = models.ForeignKey(Location, on_delete = models.CASCADE, related_name = 'position_information')

	def __str__(self):
		return self.title

	class Meta:
		ordering = ['-id']
		unique_together = ['title', 'author']




class Person(models.Model):

	def get_fullname(self):
		return '{} {}'.format(self.lastname, self.firstname)

	lastname = models.CharField(max_length=50)
	firstname = models.CharField(max_length=50)

	fullname = property(get_fullname)

	birthday = models.DateField(blank= True)
	address = models.TextField()
	phone = models.CharField(max_length = 20)

	def __str__(self):
		return '{} {}'.format(self.lastname, self.firstname)

	class Meta:
		ordering = ['-id']
		unique_together = ['lastname', 'firstname', 'birthday']



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

	book = models.ForeignKey('BookInfo', on_delete = models.CASCADE, related_name = 'book_information')
	person_subscription = models.ForeignKey('Person', on_delete = models.CASCADE, related_name = 'subscriber')
	date_of_issue = models.DateField(blank= True, default=timezone.now)
	date_of_return = models.DateField(blank= True, default=date.today() + timedelta(days=14))
	status_of_book = models.IntegerField(choices = STATUS, default = 0)

	def __str__(self):
		return self.book.title

	class Meta:
		ordering = ['-id']