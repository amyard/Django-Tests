from django.shortcuts import render

from django.views.generic import ListView, DetailView
from core.models import Movie

# Create your views here.


class MovieView(ListView):
	model = Movie

class MovieDetail(DetailView):
	model = Movie