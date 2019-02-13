from django.db import models
from django.conf import settings


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, unique = True)
	password = models.CharField(max_length = 20)

	def __str__(self):
		return self.user.username