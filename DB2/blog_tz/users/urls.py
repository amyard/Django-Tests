from django.urls import path
from .views import *

from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView


app_name = 'users'
urlpatterns = [

    # users
    path('login/', LoginView.as_view(), name ='login-view'),
    path('registration/', RegistrationView.as_view(), name = 'registration-view'),
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('posts:base-view')), name ='logout-view'),

    # profile and actions
    path('profile/<pk>', Profile.as_view(), name = 'profile'),
    path('update-profile/<pk>', ProfileUpdateView.as_view(), name = 'update-profile'),
    path('delete-profile/<pk>', ProfileDeleteView.as_view(), name = 'delete-profile'),
]

