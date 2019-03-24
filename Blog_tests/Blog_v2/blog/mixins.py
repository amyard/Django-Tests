from django.views.generic.list import MultipleObjectMixin
from .models import Tag

class TagListMixin(MultipleObjectMixin):
	def get_context_data(self, *args, **kwargs):
		context = {}
		context['tags_side'] = Tag.objects.all()
		return context