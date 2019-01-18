from django.urls import path
from blog import views
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView,
					TagListView, TagDetailView, TagCreateView, TagUpdateView, TagDeleteView)

urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),

    # TAGS
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


    # path('about/', views.about, name = 'blog-about'),
]