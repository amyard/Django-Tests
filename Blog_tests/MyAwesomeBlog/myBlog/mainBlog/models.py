from django.db import models
from django.utils import timezone

# use for get_absolute_url
from django.urls import reverse 

# для комментариев
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation



class Category(models.Model):

	name = models.CharField(max_length = 50)
	slug = models.SlugField()


	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('category-detail', kwargs = {'slug':self.slug})  # category-detail - variable from urls.py  "name"



# cохраняем картинки в media -> по категориям -> по slug
def save_image_path(instance, filename):
	filename = instance.slug + '.jpg'
	return "{}/{}/{}".format(instance.category.slug, instance.slug, filename)




class Article(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=120)
	slug = models.SlugField()
	image = models.ImageField(upload_to = save_image_path)
	content = models.TextField()

	udpated = models.DateTimeField(auto_now= True, auto_now_add = False)
	date = models.DateTimeField(blank= True, default=timezone.now)

	likes = models.PositiveIntegerField(default = 0)
	dislikes = models.PositiveIntegerField(default = 0)

	comments = GenericRelation('comments')

	# в админ панеле будет отображаются пользователи, которые поставили лайки/дизлайки
	user_reaction = models.ManyToManyField(settings.AUTH_USER_MODEL, blank = True)


	def __str__(self):
		return "{}: {}".format(self.category.name, self.title)

	def get_absolute_url(self):
		return reverse('article-detail', kwargs = {'category':self.category.slug,
													'slug':self.slug})


class Comments(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	comment = models.TextField()
	timestamps = models.DateTimeField(auto_now_add=True, auto_now=False)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')




class UserAccount(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	first_name= models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()

	favorite_article = models.ManyToManyField(Article)

	def __str__(self):
		return self.user.username

	# для личного кабинета
	# def get_abolute_url(self):
	# 	return reverse('account_view', kwargs = {'user':self.user.username})

