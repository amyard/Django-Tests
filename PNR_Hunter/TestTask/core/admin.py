from django.contrib import admin
from .models import Project,Task

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
	list_display = ['title', 'user']
	list_filter = ['user']



class TaskAdmin(admin.ModelAdmin):
	list_display = ['title','project', 'user', 'priority']
	list_filter = ['priority']
	list_editable = ['priority']

	def user(self, obj):
		return obj.project.user


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
