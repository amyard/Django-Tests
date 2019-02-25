from django.urls import path

from .views import CategoryListView, LoginView, RegistrationView

# for logout
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path('', CategoryListView.as_view(), name ='base-view'),


    # user
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('base-view')), name ='logout-view'),
    path('login/', LoginView.as_view(), name ='login-view'),
    path('registration/', RegistrationView.as_view(), name = 'registration-view'),
]

