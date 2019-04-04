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



#
# from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from django.utils.translation import ugettext_lazy as _





#
#
# class UserManager(BaseUserManager):
#
#     def create_user(self, email, password=None, **kwargs):
#         if not email:
#             raise ValueError('Email field is required')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **kwargs)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)
#
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
#     email = models.EmailField(max_length=255, unique=True)
#     city = models.CharField(max_length = 25)
#     country = models.CharField(max_length = 25)
#     birthday = models.DateTimeField(blank = True, default = timezone.now)
#
#     objects = UserManager()
#     USERNAME_FIELD = 'email'
#
#     def __str__(self):
#         return self.user.username
#
#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')
