from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


def gen_slug(s):
    new_slug = slugify(s, allow_unicode = True)
    return new_slug


def save_image_path(instance, filename):
    filename = instance.slug + '.jpg'
    date = instance.date_posted.strftime("%Y-%m-%d %H:%M:%S").split(' ')[0]
    return f'posts_pics/{date}/{instance.title}/{filename}'


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length = 255, unique = True)
    slug = models.SlugField(max_length = 150, unique = True, blank = True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default = 'default-post.png', upload_to=save_image_path, blank=True)

    class Meta:
        ordering = ('-date_posted',)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title