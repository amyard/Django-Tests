from .views import PostRUDViews, PostAPIViews
from django.urls import path



urlpatterns = [
    path('<pk>', PostRUDViews.as_view(), name = 'post-rud'),
    path('', PostAPIViews.as_view(), name = 'create-post')
]