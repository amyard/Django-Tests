from django.db import models
from django.conf import settings


# Create your models here.
class UserAccount(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, unique = True)

	def __str__(self):
		return self.user.username