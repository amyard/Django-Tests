from django.contrib import admin
from .models import City, JobDescr, Job

# Register your models here.

class CityAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'number_id']
	prepopulated_field = {'slug':('title',)}
	list_editable = ['slug']


class JobAdmin(admin.ModelAdmin):
	list_display = ['job', 'city', 'site', 'user', 'timestamp']
	list_filter = ['timestamp']
	date_hierarchy = 'timestamp'


admin.site.register(City, CityAdmin)
admin.site.register(JobDescr, JobAdmin)
admin.site.register(Job)
