from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import datetime

from django.conf import settings

# for slug
from django.utils.text import slugify

def gen_slug(s):
	new_slug = slugify(s, allow_unicode = True)
	return new_slug


class Post(models.Model):
	title = models.CharField(max_length = 150, unique = True)
	slug = models.SlugField(max_length = 150, unique = True, blank = True)
	content = models.TextField()
	date_posted = models.DateTimeField(default = timezone.now)
	author = models.ForeignKey(User, on_delete = models.CASCADE)
	tags = models.ManyToManyField('Tag', blank = True, related_name = 'posts')

	likes = models.PositiveIntegerField(default = 0)
	dislikes = models.PositiveIntegerField(default = 0)

	user_reaction = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True, related_name = 'user_reaction')

	class Meta:
		ordering = ('-date_posted',)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs = {'slug': self.slug})


class Tag(models.Model):
	title = models.CharField(max_length=50, unique = True)
	slug = models.CharField(max_length=50, unique = True, blank = True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)



	def __str__(self):
		 return self.title





class Comments(models.Model):
	post = models.ForeignKey(Post, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	content = models.TextField(max_length=200)
	timestamp = models.DateTimeField(default = datetime.datetime.now())
	reply = models.ForeignKey('Comments', null = True, related_name = 'replies', on_delete = models.CASCADE)

	def __str__(self):
		return f'{self.post.title} - {self.user.username}'