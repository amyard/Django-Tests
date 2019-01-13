from django.db import models
from django.conf import settings





# Create your models here.

class MovieManager(models.Manager):
	def all_with_related_persons(self):
		qs = self.get_queryset()
		qs = qs.select_related('director')
		qs = qs.prefetch_related('writers', 'actors')

		return qs



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

	# добавляем мудил
	director = models.ForeignKey(to='Person', on_delete = models.SET_NULL, related_name = 'directed', null = True, blank = True)
	writers =  models.ManyToManyField(to='Person', related_name = 'writing_credits', blank = True)
	actors = models.ManyToManyField(to='Person', through = 'Role', related_name = 'acting_credits', blank = True)

	objects = MovieManager()

	# обратная сортировка
	class Meta:
		ordering = ('-year', 'title')

	def __str__(self):
		return '{} ({})'.format(self.title, self.year)




# Manager for class Person
class PersonManager(models.Manager):
	def all_with_prefetch_movies(self):
		qs = self.get_queryset()

		# исп функ prefetch_related для запроса
		return qs.prefetch_related(
					'directed', 'writing_credits', 'role_set__movie'
			)


class Person(models.Model):
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length = 120)
	born = models.DateField()
	died = models.DateField(null = True, blank = True)


	objects = PersonManager()

	class Meta:
		ordering = ('last_name', 'first_name')

	def __str__(self):
		if self.died:
			return '{}, {}, ({} - {})'.format(self.last_name, self.first_name, self.born, self.died)
		else:
			return '{}, {}, ({})'.format(self.last_name, self.first_name, self.born)


# для актеров класс, дабы была связь
class Role(models.Model):
	movie = models.ForeignKey(Movie, on_delete = models.DO_NOTHING)
	person = models.ForeignKey(Person, on_delete = models.DO_NOTHING)
	name = models.CharField(max_length = 120)

	def __str__(self):
		return '{} {} {}'.format(self.movie_id, self.person_id, self.name)

	class Meta:
		unique_together = ('movie', 'person', 'name')


######################################################################################################
#####################################################################################################

class VoteManager(models.Manager):
	def get_vote_or_unsaved_blank_vote(self):
		try:
			return Vote.objects.get(movie = movie, user = user)
		except Vote.DoesNotExist:
			# create new model in memory, not in db. for saving - use save() method
			return Vote(movie = movie, user = user)



class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = (
        (UP, "👍",),
        (DOWN, "👎",),
    )

    value = models.SmallIntegerField(choices = VALUE_CHOICES, )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    voted_on = models.DateTimeField(auto_now = True)

    objects = VoteManager()

    class Meta:
    	unique_together = ('user', 'movie')