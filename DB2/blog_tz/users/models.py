from django.db import models
from django.conf import settings
from PIL import Image
from django.utils import timezone



def save_image_path(instance, filename):
    filename = instance.image
    return 'profile_pics/{}/{}'.format(instance.user.username, filename)



class Subscriber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True, related_name = 'user')
    city = models.CharField(max_length = 25)
    country = models.CharField(max_length = 25)
    birthday = models.DateField(blank = True, default = timezone.now)
    image = models.ImageField(default='default.jpg', upload_to=save_image_path, blank = True)


    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # resize of image
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-id']