from django.db import models





# Create your models here.

class Movie(models.Model):
	NOT_RATED = 0
	RATED_G = 1
	RATED_PG = 2
	RATED_R = 3
	RATINGS = (
			(NOT_RATED, 'NR - Not Rated'),
			(RATED_G, 'G - General Audiences'),
			(RATED_PG, 'PG - Parental Guidance'),
			(RATED_R, 'R - Restricted'),
		)

	title = models.CharField(max_length = 120)

	# описание
	plot = models.TextField()

	# год выпуска
	year = models.PositiveIntegerField()
	rating = models.IntegerField(choices = RATINGS, default = NOT_RATED)

	# длительность
	runtime = models.PositiveIntegerField()
	website = models.URLField(blank = True)

	# обратная сортировка
	class Meta:
		ordering = ('-year', 'title')

	def __str__(self):
		return '{} ({})'.format(self.title, self.year)