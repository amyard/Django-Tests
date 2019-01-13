from django.urls import path

from core import views

app_name = 'core'
urlpatterns = [
	# path('movies', views.MovieView.as_view(), name = 'MovieList'),
	path('', views.MovieView.as_view(), name = 'MovieList'),
	path('movie/<int:pk>', views.MovieDetail.as_view(), name = 'MovieDetail'),

	# vote views
	path('movie/<int:movie_id>/vote', views.CreateVote.as_view(), name = 'CreateVote'),
	path('movie/<int:movie_id>/vote/<int:pk>', views.UpdateVote.as_view(), name = 'UpdateVote'),
]