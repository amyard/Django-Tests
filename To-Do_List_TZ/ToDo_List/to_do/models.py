from django.db import models
from django.conf import settings 
from django.utils import timezone


class Project(models.Model):
	name = models.CharField(max_length = 150)
	color = models.CharField(max_length = 20)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'user', blank = True)

	def __str__(self):
		return self.name



class Task(models.Model):
	HIGH = -1
	MIDDLE = 0
	LOW = 1
	PRIORITY = ((HIGH, 'red'),(MIDDLE, 'yellow'),(LOW, 'white'))

	COMPLETED = 1
	UNCOMPLETED = 0
	STATUS = ((COMPLETED, 'Completed'),(UNCOMPLETED, 'Uncompleted'))

	project = models.ForeignKey(Project, on_delete = models.CASCADE, related_name = 'project')
	title = models.CharField(max_length = 150)
	priority = models.IntegerField(choices = PRIORITY, default = MIDDLE)
	status = models.IntegerField(choices = STATUS, default = UNCOMPLETED)
	timestamp = models.DateTimeField(blank = True, default = timezone.now)

	def __str__(self):
		return f'{self.title}'

	class Meta:
		ordering = ['priority']