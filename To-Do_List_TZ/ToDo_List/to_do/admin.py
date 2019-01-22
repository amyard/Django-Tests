from django.contrib import admin
from .models import Project, Task


class ProjectAdmin(admin.ModelAdmin):
	list_display = ('name', 'user',)




class TaskAdmin(admin.ModelAdmin):
	# inlines = [ProjectInline]
	list_display = ['title','project', 'user', 'timestamp', 'priority', 'status']
	list_filter = ['timestamp', 'priority', 'status']
	list_editable = ['priority', 'status']
	date_hierarchy = 'timestamp'

	def user(self, obj):
		return obj.project.user

# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)