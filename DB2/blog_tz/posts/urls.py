from django.urls import path
from .views import *

from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', MainTestView.as_view(), name = 'base-view'),

]