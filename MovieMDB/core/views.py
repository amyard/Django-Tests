from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from core.models import Movie, Person, Vote

# for vote views
from django.urls import reverse
from core.forms import VoteForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


# Create your views here.


class MovieView(ListView):
	model = Movie



class MovieDetail(DetailView):
	queryset = Movie.objects.all_with_related_persons()

	# vote
	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			vote = Vote.objects.get_vote_or_unsaved_blank_vote(movie = self.object, user = self.request.user)

			if vote.id:
				vote_form_url = reverse('core:UpdateVote', kwargs = {'movie_id':vote.movie.id, 'pk':vote.id})
			else:
				vote_form_url = reverse('core:CreateVote', kwargs = {'movie_id':self.object.id})
			vote_form = VoteForm(instance = vote)
			ctx['vote_form'] = vote_form
			ctx['vote_form_url'] = vote_form_url
		return ctx


class CreateVote(LoginRequiredMixin, CreateView):
	from_class = VoteForm

	def get_initial(self):
		initial = super().get_initial()
		initial['user'] = self.request.user.id
		initial['movie'] = self.kwargs['movie_id']
		return initial

	def get_success_url(self):
		movie_id = self.object.movie.id
		return reverse('core:MovieDetail', kwargs = {'pk':movie_id})

	def render_to_response(self, context, **response_kwargs):
		movie_id = context['object'].id
		movie_detail_url = reverse('core:MovieDetail', kwargs = {'pk':movie_id})
		return redirect(to = movie_detail_url)


class UpdateVote(LoginRequiredMixin, UpdateView):
	form_class = VoteForm
	queryset = Vote.objects.all()

	def get_object(self, queryset = None):
		vote = super().get_object(queryset)
		user = self.request.user
		if vote.user != user:
			raise PermissionDenied('Cannot change another user vote')
		return vote

	def get_success_url(self):
		movie_id = selg.object.movie.id
		return reverse('core:MovieDetail', kwargs = {'pk':movie_id})

	def render_to_response(self, context, **response_kwargs):
		movie_id = context['object'].id
		movie_detail_url = reverse('core:MovieDetail', kwargs = {'pk':movie_id})
		return redirect(to = movie_detail_url)



class PersonDetail(DetailView):
	queryset = Person.objects.all_with_prefetch_movies()
