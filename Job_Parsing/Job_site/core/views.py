from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import City, JobDescr
from .forms import CityForm, JobForm





#####################################################################################
######################################  ADD CITIE    ################################
#####################################################################################


class CityCreateView(LoginRequiredMixin, CreateView):
	form = CityForm
	fields = '__all__'
	success_url = '/'
	queryset = City.objects.all()
	template_name = 'core/create.html'

	def form_valid(self, form):
		print(form.cleaned_data)
		return super().form_valid(form)

	def test_func(self):
		city = self.get_object()
		if self.request.user == user.is_superuser:
			return True
		return False



#####################################################################################
######################################  LIST VIEW    ################################
#####################################################################################


class MainHome(ListView):
	model = JobDescr
	form = JobForm
	template_name = 'core/base.html'

	def get_context_data(self, *args, **kwargs):
		context = super(MainHome, self).get_context_data( *args, **kwargs)
		context['form'] = self.form
		context['jobs'] = self.model.objects.all()
		return context

	def form_invalid(self, form, **kwargs):
		return self.render_to_response(self.get_context_data({'form':form}))


	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)

		if form.is_valid():
			user = self.request.user
			job = form.cleaned_data['job']
			city = form.cleaned_data['city']
			site = form.cleaned_data['site']

			if request.user.is_authenticated:
				job = self.model.objects.create(job = job, city = city, site = site, user = user)
				job.save()
				
			slug = City.objects.values_list('slug', flat=True).get(title = city)
			number_id = City.objects.values_list('number_id', flat=True).get(title = city)

			# для работа надо отправить job, site, number_id - для неправильных адресов   job = для правильных
			print(slug)
			print(number_id)
			print(job)
			print(city)
			print(site)
			return render(self.request, self.template_name, context = {'form':form, 'city': city})
		context = {
			'form':form, 
			'city': city
		}
		return render(self.request, self.template_name, context)



