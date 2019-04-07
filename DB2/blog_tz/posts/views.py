from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin

from bootstrap_modal_forms.generic import (BSModalDeleteView)

from .models import Post, Comments
from users.models import Subscriber
from .forms import CommentForm



class MainTestView(ListView):
	template_name = 'posts/main.html'
	model = Post
	paginate_by = 2

	def get_queryset(self):
		return self.model.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(MainTestView, self).get_context_data(*args, **kwargs)
		context['user'] = self.request.user
		try:
			profile = Subscriber.objects.get(user = self.request.user)
			context['profile'] = profile
			if profile.city == '':
				context['need_data'] = True
			else:
				context['need_data'] = False
		except:
			context['profile'] = None
			context['need_data'] = False

		context['data'] = self.get_queryset()

		p = Paginator(self.get_queryset(), self.paginate_by)
		context['posts'] = p.page(context['page_obj'].number)
		return context





class PostDetailView(FormMixin, DetailView):
	template_name = 'posts/detail.html'
	model = Post
	form_class = CommentForm

	def get_success_url(self):
		return reverse('posts:detail-post', kwargs={'slug': self.object.slug})

	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)
		context['post'] = self.get_object()
		context['form'] = self.form_class

		context['comments'] = Comments.objects.filter(post=self.get_object()).order_by('-id')

		uniq = Comments.objects.filter(post=self.get_object()).order_by().values_list('user', flat=True).distinct()
		context['profile'] = Subscriber.objects.filter(user__id__in=uniq)
		return context

	def post(self, request, *args, **kwargs):
		form = CommentForm(request.POST or None)
		if form.is_valid():
			content = request.POST.get('content')
			comment = Comments.objects.create(post=self.get_object(), user=request.user, content=content)
			comment.save()
			return HttpResponseRedirect(reverse('posts:detail-post', kwargs={'slug': kwargs.get('slug')}))






class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'slug', 'content', 'image']
	template_name = 'posts/actions/post-create.html'
	success_message = 'Success: Post was created.'
	success_url = reverse_lazy('posts:base-view')

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)




class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'slug', 'content', 'image']
	template_name = 'posts/actions/post-create.html'
	success_message = 'Success: Post was updated.'
	success_url = reverse_lazy('posts:base-view')

	def get_success_url(self):
		obj = self.kwargs['slug']
		return reverse('posts:detail-post', kwargs={'slug': obj})

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author or self.request.user == user.is_superuser:
			return True
		return False



class BookDeleteView(BSModalDeleteView):
    model = Post
    template_name = 'posts/actions/post-delete.html'
    success_message = 'Success: Post was deleted.'
    success_url = reverse_lazy('posts:base-view')