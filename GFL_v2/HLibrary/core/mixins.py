from datetime import date, timedelta
from .models import (Books, Genre, Location, Person, BookInfo, )



class ListMixins():
	queryset = None
	template_name = None
	title = None
	title_content = None


	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['books'] = self.queryset
		context['title'] = self.title
		context['title_content'] = self.title_content
		
		return context