from django.conf.urls import url

# for logout
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView

# our views
from mainBlog.views import (CategoryListView, 
							CategoryDetailView, 
							ArticleDetailView, 
							DynamicArticleImageView, 
							CreateCommentView, 
							DisplayArticleByCategoryView, 
							UserReactionView,
							RegistrationView,
							LoginView,
							#UserAccountView
							SearchView,
							)


urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name = 'base_view'),
    url(r'^category/(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name = 'category-detail'),
    url(r'^(?P<category>[-\w]+)/(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name = 'article-detail'),
    url(r'^show_article_image/$', DynamicArticleImageView.as_view(), name = 'article-image'),
    url(r'^add_comment/$', CreateCommentView.as_view(), name = 'add_comment'),
    url(r'^display_articles_by_category/$', DisplayArticleByCategoryView.as_view(), name = 'articles_by_category'),
    url(r'^user_reaction/$', UserReactionView.as_view(), name = 'user_reaction'),
    url(r'^registration/$', RegistrationView.as_view(), name = 'registration'),
    url(r'^login/$', LoginView.as_view(), name = 'login_view'),
    #url(r'^user_account/(?P<user>[-\w]+)/$', UserAccountView.as_view(), name = 'account_view')
    #url(r'^user_account/(?P<user>[-\w]+)/$', UserAccountView.as_view(), name = 'account_view')
    url(r'^logout/$', LogoutView.as_view(next_page = reverse_lazy('base_view')), name = 'logout_view' ),
    url(r'^search/$', SearchView.as_view(), name = 'search_view')

]