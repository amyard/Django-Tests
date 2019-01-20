from django.urls import path
from blog import views
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView,
					TagListView, TagDetailView, TagCreateView, TagUpdateView, TagDeleteView,
                    SearchView, UserReactionView,)

urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),

    # TAGS - сделать отдельное APP для тегов и закинуть туда эти url
    path('tags/', TagListView.as_view(), name = 'tags'),
    path('tags/new/', TagCreateView.as_view(), name = 'tag-create'),
    path('tags/<str:slug>', TagDetailView.as_view(), name = 'tag-detail'),
    path('tags/<str:slug>/update/', TagUpdateView.as_view(), name = 'tag-update'),
    path('tags/<str:slug>/delete/', TagDeleteView.as_view(), name = 'tag-delete'),

    # USER
    path('user/<str:username>', UserPostListView.as_view(), name = 'user-posts'),

    #POST
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('post/<str:slug>/', PostDetailView.as_view(), name = 'post-detail'),    
    path('post/<slug>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<slug>/delete/', PostDeleteView.as_view(), name = 'post-delete'),


    # SEARCH
    path('search/', SearchView.as_view(), name = 'search_view'),

    path('user_reaction/', UserReactionView.as_view(), name = 'user_reaction'),

]