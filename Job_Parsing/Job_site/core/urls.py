from django.urls import path, include
from .views import (MainHome,  LoginView, RegistrationView,
					CityCreateView, CityDelete, CityUpdate,
			)

from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', MainHome.as_view(), name = 'base_view'),

    # city
    path('create-city/', CityCreateView.as_view(), name='create-city'),
    path('delete-city/<pk>-<title>', CityDelete.as_view(), name='delete-city'),
	path('update-city/<pk>-<title>', CityUpdate.as_view(), name='update-city'),


    # users
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('base_view')), name = 'logout_view'),
    path('registration/', RegistrationView.as_view(), name = 'registration'),
]