from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.core.paginator import Paginator
from django.contrib.auth.models import User



def about(request):
	return render(request, 'blog/about.html', {'title':'About'})



class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	paginate_by = 10


	def get_context_data(self, *args, **kwargs):
		context = super(PostListView, self).get_context_data(*args, **kwargs)

		p = Paginator(Post.objects.select_related().all(), self.paginate_by)
		context['posts'] = p.page(context['page_obj'].number)
		context['user'] = self.request.user
		return context


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 10

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author = user)




# page_obj

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