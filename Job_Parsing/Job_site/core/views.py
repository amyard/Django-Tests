from django.shortcuts import render
from django.http import HttpResponse



# Create your views here.
def home(requests):
	return HttpResponse('<h1>Scorpion Wins!!!</h1>')