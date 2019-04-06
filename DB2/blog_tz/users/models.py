from django.db import models
from django.conf import settings
from django.utils import timezone



class Subscriber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    city = models.CharField(max_length = 25)
    country = models.CharField(max_length = 25)
    birthday = models.DateField(blank = True, default = timezone.now)


    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-id']