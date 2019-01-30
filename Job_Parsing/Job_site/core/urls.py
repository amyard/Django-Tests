from django.urls import path, include
from .views import MainHome, CityCreateView

from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', MainHome.as_view(), name = 'base_view'),
    path('create-city/', CityCreateView.as_view(), name='create-city'),


    # users
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('base_view')), name = 'logout_view'),
]