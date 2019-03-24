from django.db import models
from django.conf import settings


# Create your models here.
class Project(models.Model):
	title = models.CharField(max_length = 30)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'user', blank = True)

	def __str__(self):
		return f'{self.title}'

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'



class Task(models.Model):
	HIGH = -1
	MIDDLE = 0
	LOW = 1
	PRIORITY = ((HIGH, 'Высокий'),(MIDDLE, 'Средний'),(LOW, 'Низкий'))

	title = models.CharField(max_length = 70)
	description = models.TextField()
	priority = models.IntegerField(choices = PRIORITY, default = HIGH)
	project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = 'project')

	def __str__(self):
		return f'{self.title}'

	class Meta:
		verbose_name = 'Задание'
		verbose_name_plural = 'Задания'
		ordering = ['id']