from django.urls import path
from user import views


# including logging in/out, changing/reset password
from django.contrib.auth import views as auth_views

app_name = 'user'
urlpatterns = [
	path('register', views.RegistrationView.as_view(), name = 'register'),
	path('login/', auth_views.LoginView.as_view(), name = 'login'),
	path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
]