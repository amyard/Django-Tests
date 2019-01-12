from django.shortcuts import render


# для работы с нашими данными
from django.views.generic.list import ListView
from mainBlog.models import Article, Category, UserAccount

# работаем с отдельными компонентами
from django.views.generic.detail import DetailView

# для отображение категорий в header
from mainBlog.mixins import CategoryAndArticlesListMixin

# для отображения картинок при наведении мышкой
from django.http import JsonResponse
from django.views import View

# для комментариев
from mainBlog.forms import CommentForm, ResistrationForm, LoginForm

# для работы с ошибками при заполнении регистрации
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponseRedirect

# for search view
from django.db.models import Q



# отображает все наши атрибуты
class ArticleListView(ListView):
	model = Article
	template_name = 'index.html'

	# функ загружает все данные из Article
	def get_context_data(self, *args, **kwargs):
		context = super(ArticleListView, self).get_context_data(*args, **kwargs)
		context['articles'] = self.model.objects.all()
		return context


class CategoryListView(ListView, CategoryAndArticlesListMixin):
	model = Category
	template_name = 'index.html'

	# функ загружает все данные из Article
	def get_context_data(self, *args, **kwargs):
		context = super(CategoryListView, self).get_context_data(*args, **kwargs)
		context['categories'] = self.model.objects.all()

		# выдает рандомные 3 статьи
		context['slider_articles'] = Article.objects.order_by('?')[:5]

		# отображаем последние 5 статьей.
		context['articles'] = Article.objects.all().order_by('-likes')[:7]
		
		context['article'] = Article.objects.latest('id')
		return context





# создаем класс для отображение каждой категории отдельно
class CategoryDetailView(DetailView, CategoryAndArticlesListMixin):
	model = Category
	template_name = 'category_detail.html'

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		context['category'] = self.get_object()

		# отображаем все статтьи по категории
		context['articles_from_category'] = self.get_object().article_set.all()
		return context	


class ArticleDetailView(DetailView, CategoryAndArticlesListMixin):
	model = Article
	template_name = 'article_detail.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
		context['article'] = self.get_object()
		context['article_comments'] = self.get_object().comments.all().order_by('-timestamps')
		context['form'] = CommentForm()
		return context	


# при наведении мышки меняет картинки
class DynamicArticleImageView(View):
	def get(self, *args, **kwargs):
		article_id = self.request.GET.get('article_id')
		article = Article.objects.get(id = article_id)
		data = {
			'article_image': article.image.url
		}
		return JsonResponse(data)

# для создания комментов
class CreateCommentView(View):
	template_name = 'article_detail.html'

	def post(self, request, *args, **kwargs):
		article_id = self.request.POST.get('article_id')
		comment = self.request.POST.get('comment')
		article = Article.objects.get(id = article_id)
		new_comment = article.comments.create(author = request.user, comment = comment)
		comment = [{'author':new_comment.author.username, 'comment': new_comment.comment, 'timestamps':new_comment.timestamps.strftime('%Y-%m-%d %H:%m')}]
		return JsonResponse(comment, safe = False)


# для отображения статьей по табам
class DisplayArticleByCategoryView(View):
	template_name = 'index.html'

	def get(self, request, *args, **kwargs):
		category_slug = self.request.GET.get('category_slug')
		articles = list(Article.objects.filter(category = Category.objects.get(slug = category_slug)).values('title', 'image', 'slug'))
		# the same queryset
		#acticles_ = list(Category.objects.get(slug = category_slug).article_set.all().values('title', 'image', 'slug'))

		data = {
			'articles':articles
		}
		return JsonResponse(data)



# для лайков и дизлайков

class UserReactionView(View):
	template_name = 'article_detail.html'

	def get(self, request, *args, **kwargs):
		article_id = self.request.GET.get('article_id')
		article = Article.objects.get(id = article_id)
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


# регистрация

User = get_user_model()


class RegistrationView(View):
	template_name = 'registration.html'

	def get(self,request,*args,**kwargs):
		form = ResistrationForm()
		categories = Category.objects.all()
		context = {
				'form':form,
				'categories': categories
		}

		return render(self.request, self.template_name, context)

	# работа с ошибками при заполнении формы
	def post(self, request, *args,**kwargs):
		form = ResistrationForm(request.POST or None)
		if form.is_valid():
			new_user = form.save(commit = False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			new_user.set_password(password)
			password_check = form.cleaned_data['password_check']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			new_user.save()
			UserAccount.objects.create(user = User.objects.get(username = new_user.username),
										first_name = new_user.first_name,
										last_name = new_user.last_name,
										email = new_user.email)

			return HttpResponseRedirect('/')
		context = {
				'form':form
		}

		return render(self.request, self.template_name, context)



class LoginView(View):
	template_name = 'login.html'

	def get(self,request,*args,**kwargs):
		categories = Category.objects.all()
		form = LoginForm()
		context = {
				'form':form,
				'categories':categories
		}

		return render(self.request, self.template_name, context)

	# работа с ошибками при заполнении формы
	def post(self, request, *args,**kwargs):
		form = LoginForm(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user:
				login(self.request, user)
			
			return HttpResponseRedirect('/')
		context = {
				'form':form
		}

		return render(self.request, self.template_name, context)


# class UserAccountView(View):
# 	template_name = 'user_account.html'
# 	def get(self,request, *args, **kwargs):
# 		user = self.kwargs.get('user')
# 		current_user = UserAccount.objects.get(user = User.objects.get(username = user))
# 		context = {
# 			'current_user':current_user
# 		}

# 		return render(self.request, self.template_name, context)

# for search button
class SearchView(View):
	template_name='search.html'

	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('q')
		categories = Category.objects.all()
		founded_articles = Article.objects.filter(
								Q(title__icontains = query)|
								Q(content__icontains = query)
							)

		context = {
			'founded_articles':founded_articles,
			'categories':categories
		}

		return render(self.request, self.template_name, context)
