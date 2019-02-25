from django.db import models
from django.conf import settings


# Create your models here.
class Project(models.Model):
	title = models.CharField(max_length = 30)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'user', blank = True)

	def __str__(self):
		return f'{self.title} - {self.user.username}'