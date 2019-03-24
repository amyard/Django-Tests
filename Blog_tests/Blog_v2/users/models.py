from django.db import models
from django.contrib.auth.models import User 
from PIL import Image


def save_image_path(instance, filename):
	filename = instance.image
	return 'profile_pics/{}/{}'.format(instance.user.username, filename)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	image = models.ImageField(default = 'default.jpg', upload_to = save_image_path)

	def __str__(self):
		return f'{self.user.username} Profile'


	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		# resize of image
		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)