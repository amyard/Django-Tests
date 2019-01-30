from django.urls import path, include
from .views import (MainHome,  LoginView, RegistrationView,
					CityCreateView,
			)

from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', MainHome.as_view(), name = 'base_view'),
    path('create-city/', CityCreateView.as_view(), name='create-city'),


    # users
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('base_view')), name = 'logout_view'),
    path('registration/', RegistrationView.as_view(), name = 'registration'),
]