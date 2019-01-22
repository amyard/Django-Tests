from django.urls import path
from .views import (home, 
					LoginView, RegistrationView,
	)

# for logout
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', home, name = 'base_view'),
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('base_view')), name = 'logout_view'),
    path('login/', LoginView.as_view(), name = 'login_view'),
    path('registration/', RegistrationView.as_view(), name = 'registration')
]
