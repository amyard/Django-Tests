from django.urls import path
from .views import *

from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', MainTestView, name = 'base-view'),

    # # users
    # path('login/', LoginView.as_view(), name ='login-view'),
    # path('registration/', RegistrationView.as_view(), name = 'registration-view'),
    # path('logout/', LogoutView.as_view(next_page = reverse_lazy('base-view')), name ='logout-view'),
]