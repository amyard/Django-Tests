from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator


from .models import Post
from users.models import Subscriber


# def MainTestView(request):
# 	try:
# 		profile = Subscriber.objects.get(user = request.user)
# 		return render(request, 'posts/main.html', {'info': 'We have all info about user right now', 'user': request.user, 'profile':profile})
# 	except:
# 		return render(request, 'posts/main.html', {'info':'We have all info about user right now', 'user': request.user})



class MainTestView(ListView):
	template_name = 'posts/main.html'
	model = Post
	paginate_by = 2

	def get_queryset(self):
		return self.model.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(MainTestView, self).get_context_data(*args, **kwargs)
		context['user'] = self.request.user
		context['data'] = self.get_queryset()

		p = Paginator(self.get_queryset(), self.paginate_by)
		context['posts'] = p.page(context['page_obj'].number)
		return context



class PostDetailView(DetailView):
	template_name = 'posts/detail.html'
	model = Post

	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)
		context['post'] = self.get_object()
		return context