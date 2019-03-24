from django.contrib import admin
from .models import (Books,
					Genre,
					Location,
					Person,
					BookInfo
	)


class BookAdmin(admin.ModelAdmin):
	list_display = ['id', 'book','date_of_issue', 'date_of_return', 'status_of_book']
	list_filter = ['date_of_issue', 'date_of_return', 'status_of_book']
	list_editable = ['status_of_book']
	search_fields = ['book']
	list_display_links = ['book']


class locationAdmin(admin.ModelAdmin):
	list_display = ['id', 'room','bookcase', 'shelf']


# Register your models here.
admin.site.register(Books,BookAdmin)
admin.site.register(Genre)
admin.site.register(Location, locationAdmin)
admin.site.register(Person)
admin.site.register(BookInfo)