from django.urls import path

from core import views

app_name = 'core'
urlpatterns = [
	path('movies', views.MovieView.as_view(), name = 'MovieList'),
	path('movie/<int:pk>', views.MovieDetail.as_view(), name = 'MovieDetail'),
]