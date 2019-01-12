from django.shortcuts import render

from django.views.generic import ListView, DetailView
from core.models import Movie, Person

# Create your views here.


class MovieView(ListView):
	model = Movie

class MovieDetail(DetailView):
	queryset = Movie.objects.all_with_related_persons()

class PersonDetail(DetailView):
	queryset = Person.objects.all_with_prefetch_movies()