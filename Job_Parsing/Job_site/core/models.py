from django.db import models
from django.utils import timezone
from django.conf import settings
from users.models import Subscriber

# Автоматичесий слаг с кирилици на латиницу
from django.utils.text import slugify
from pytils import translit
import pytils

def gen_slug(x):
	new_slug = translit.translify(slugify(x, allow_unicode = True))
	return new_slug


# Create your models here.
class City(models.Model):
	title = models.CharField(max_length = 50, unique = True)
	slug = models.SlugField(unique=True, max_length = 50, blank = True)
	number_id = models.PositiveIntegerField(unique = True)

	def __str__(self):
		return self.title 

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)\

	class Meta:
		ordering = ('number_id', )


class JobDescr(models.Model):
	RABOTA = 0
	WORK = 1
	WEB_SITES = ((RABOTA, 'rabota.ua'), (WORK, 'work.ua'))

	job = models.CharField(max_length=70)
	city = models.ForeignKey(City, on_delete = models.DO_NOTHING, related_name = 'city')
	site = models.IntegerField(choices = WEB_SITES, default = RABOTA)
	timestamp = models.DateTimeField(blank = True, default = timezone.now)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'user',
							 blank = True)


	def __str__(self):
		return self.job