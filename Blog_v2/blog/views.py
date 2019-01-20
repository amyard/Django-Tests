from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Post, Tag, Comments

from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, View, )
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.core.paginator import Paginator
from django.contrib.auth.models import User

from .forms import TagForm, CommentForm

from django.db.models import Q

from django.views.generic.edit import FormMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse





# def about(request):
# 	return render(request, 'blog/about.html', {'title':'About'})


#############################################################################
###########################        TAGS VIEWS     ###########################
#############################################################################

from django.db.models import Count

class TagListView(ListView):
	model = Tag
	template_name = 'blog/tags.html'

	def get_context_data(self, *args, **kwargs):
		context = super(TagListView, self).get_context_data(*args, **kwargs)
		context['tags'] = self.model.objects.all()
		# context['counted'] = self.model.objects.all().values('title').distinct()
		context['counted'] = Post.objects.values('tags__title').order_by('tags__title').annotate(count = Count('tags__title'))
		return context


class TagDetailView(DetailView):
	model = Tag
	template_name = 'blog/tag_detail.html'

	def get_context_data(self, *args, **kwargs):
		context = super(TagDetailView, self).get_context_data(*args, **kwargs)
		context['tag'] = self.get_object()
		context['detail_tag'] = True
		return context 


# try create and update with View
class TagCreateView(LoginRequiredMixin, View):
	def get(self, request):
		form = TagForm
		return render(request, 'blog/tag_create.html', context = {'form':form})

	def post(self, request):
		bound_form = TagForm(request.POST)
		if bound_form.is_valid():
			new_tag = bound_form.save()
			return redirect('/tags/')
		return render(request, 'blog/tag_create.html', context = {'form':bound_form})



# Only superusers can update and delete tags
class TagUpdateView(LoginRequiredMixin, View):
	def get(self, request, slug):
		tag = Tag.objects.get(slug__iexact = slug)
		bound_form = TagForm(instance = tag)
		return render(request, 'blog/tag_update_form.html', context = {'form':bound_form, 'tag':tag})

	def post(self, request, slug):
		tag = Tag.objects.get(slug__iexact = slug)
		bound_form = TagForm(request.POST, instance = tag)
		if bound_form.is_valid():
			new_tag = bound_form.save()
			return redirect('/tags/')
		return render(request, 'blog/tag_update_form.html', context = {'form':bound_form, 'tag':tag})


class TagDeleteView(View):
	def get(self, request, slug):
		tag = Tag.objects.get(slug__iexact = slug)
		return render(request, 'blog/tag_confirm_delete.html', context = {'tag': tag})

	def post(self, request, slug):
		tag = Tag.objects.get(slug__iexact = slug)
		tag.delete()
		return redirect('/tags/')

#############################################################################
###########################        POST VIEWS     ###########################
#############################################################################


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	paginate_by = 5


	def get_context_data(self, *args, **kwargs):
		context = super(PostListView, self).get_context_data(*args, **kwargs)

		p = Paginator(Post.objects.select_related().all(), self.paginate_by)
		context['posts'] = p.page(context['page_obj'].number)
		context['user'] = self.request.user
		context['tags_sidebar'] = Tag.objects.all()
		return context


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 3

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author = user)



class PostDetailView(FormMixin, DetailView):
	model = Post
	template_name = 'blog/post_detail.html'
	form_class  = CommentForm

	def get_success_url(self):
		return reverse('post-detail', kwargs={'slug': self.object.slug})


	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)
		# context['object'] = self.get_object()
		context['article'] = self.get_object()
		context['comments'] = Comments.objects.filter(post = self.get_object()).order_by('-id')
		context['detail_post'] = True
		context['form'] = self.get_form()
		return context

	def post(self, request, *args, **kwargs):

		form = CommentForm(request.POST or None)
		if form.is_valid():
			content = request.POST.get('content')
			comment = Comments.objects.create(post = self.get_object(), user = request.user, content = content)
			comment.save()
			return HttpResponseRedirect(reverse('post-detail', kwargs={'slug': self.get_object().slug}))
			





class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'slug', 'content', 'tags']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'slug', 'content', 'tags']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	# закинуть сюда суперюзера надо еще
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author or self.request.user == user.is_superuser:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	# закинуть сюда суперюзера надо еще
	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author or self.request.user == user.is_superuser:
			return True
		return False



#############################################################################
###########################        Search view     ###########################
#############################################################################


class SearchView(View):
	template_name='blog/search.html'

	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('q')
		founded_posts = Post.objects.filter(
								Q(title__icontains = query)|
								Q(content__icontains = query)
							)

		context = {
			'founded_posts':founded_posts
		}

		return render(self.request, self.template_name, context)



#############################################################################
###########################     Add likes/dislikes     ###########################
#############################################################################

class UserReactionView(View):
	template_name = 'blog/post_detail.html'

	def get(self, request, *args, **kwargs):
		article_id = self.request.GET.get('article_id')
		article = Post.objects.get(id = article_id)
		like = self.request.GET.get('like')
		dislike = self.request.GET.get('dislike')

		# пользователь может проголосовать только один раз
		if like and (request.user not in article.user_reaction.all()):
			article.likes +=1
			article.user_reaction.add(request.user)
			article.save()

		if dislike and (request.user not in article.user_reaction.all()):
			article.dislikes +=1
			article.user_reaction.add(request.user)
			article.save()

		data = {
			'likes': article.likes,
			'dislikes': article.dislikes
		}


		return JsonResponse(data)
		# return JsonResponse({'ok':'ok'})