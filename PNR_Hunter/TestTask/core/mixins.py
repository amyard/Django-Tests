from django.views.generic.list import MultipleObjectMixin
from django.core.paginator import Paginator
from .forms import *


class DeleteMixin(MultipleObjectMixin):
	model = None

	def get(self, *args, **kwargs):
		return self.post(*args, **kwargs)

	def get_success_url(self, **kwargs):
		return self.request.META.get('HTTP_REFERER')

