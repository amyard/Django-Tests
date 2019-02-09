from django.urls import path
from .views import *

# users
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', GeneralList.as_view(), name = 'base_view'),

    # users
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('base_view')), name = 'logout_view'),
    path('registration/', RegistrationView.as_view(), name = 'registration'),
]