from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin



# def home(request):
# 	context = {
# 		'posts':Post.objects.all()
# 	}
# 	return render(request, 'blog/home.html', context)

def about(request):
	return render(request, 'blog/about.html', {'title':'About'})



class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'

	def get_context_data(self, *args, **kwargs):
		context = super(PostListView, self).get_context_data(*args, **kwargs)
		context['posts'] = self.model.objects.all()
		context['user'] = self.request.user
		return context


class PostDetailView(DetailView):
	model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	# закинуть сюда суперюзера надо еще
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	# закинуть сюда суперюзера надо еще
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False