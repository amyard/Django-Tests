from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (CreateView, ListView, DeleteView,)
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import City, JobDescr, Job
from .forms import CityForm, JobForm

from users.forms import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, get_user_model
from users.models import Subscriber
from django.db.models import Q

from core.scripts.mainscript import main_script


#####################################################################################
######################################  ADD CITY    ################################
#####################################################################################




class CityCreateView(ListView):
	model = City
	template_name = 'core/create.html'
	form = CityForm
	buttom_title = 'Add city'

	def get_context_data(self, *args, **kwargs):
		context = super(CityCreateView, self).get_context_data(*args, **kwargs)
		context['cities'] = self.model.objects.all()
		context['form'] = self.form
		context['buttom_title'] = self.buttom_title
		return context	

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		cities = self.model.objects.all()
		if form.is_valid():
			title = form.cleaned_data['title']
			slug = form.cleaned_data['slug']
			number_id = form.cleaned_data['number_id']
			city = self.model.objects.create(title = title, slug = slug, number_id = number_id)
			city.save()
			return HttpResponseRedirect('../create-city')
		return render(self.request, self.template_name, context = {'form':form, 'cities': cities})


#####################################################################################
###################################   DELETE CITY    ################################
#####################################################################################



class CityDelete(DeleteView):
	model = City 

	def get(self, *args, **kwargs):
		return self.post(*args, **kwargs)

	def get_success_url(self, **kwargs):
		return self.request.META.get('HTTP_REFERER')



#####################################################################################
###################################   UPDATE CITY    ################################
#####################################################################################



class CityUpdate(View):
	model = City
	template_name = 'core/create.html'
	form = CityForm
	buttom_title = 'Edit'

	def get(self, request, *args, **kwargs):
		pk = self.kwargs.get('pk')
		title = self.kwargs.get('title')
		city = self.model.objects.get(pk = pk, title = title)
		cities = self.model.objects.all()
		form = self.form(instance = city)
		self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
		return render(self.request, self.template_name, context = {'form':form, 'cities':cities, 'buttom_title':self.buttom_title})

	def post(self, request, **kwargs):
		pk = self.kwargs.get('pk')
		cities = self.model.objects.all()
		city = self.model.objects.get(pk = pk)
		form = self.form(request.POST, instance = city)
		if form.is_valid():
			new_city = form.save()
			return HttpResponseRedirect(self.request.session.get('report_url'))
		return render(request, self.template_name, context = {'form':form})



#####################################################################################
######################################     LOGIN     ################################
#####################################################################################
User = get_user_model()


class LoginView(View):
	template_name = 'users/login.html'
	form = LoginForm

	def get(self, request, *args, **kwargs):
		form = self.form
		return render(request, self.template_name, context = {'form':form})

	def post(self, request, *args,**kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			sub = authenticate(username=username, password=password)
			if sub:
				login(self.request, sub)	
			return HttpResponseRedirect('/')
		context = {
				'form':form
		}
		return render(self.request, self.template_name, context)



#####################################################################################
######################################  REGISTRATION  ###############################
#####################################################################################

class RegistrationView(View):
	template_name = 'users/registration.html'
	form = RegistrationForm

	def get(self, request,*args,**kwargs):
		form = self.form
		context = {
				'form':form
		}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			new_user = form.save(commit = False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			new_user.set_password(password)
			password_check = form.cleaned_data['password_check']
			new_user.save()
			Subscriber.objects.create(user = User.objects.get(username=new_user.username))
			return HttpResponseRedirect('../login')
		context = {
			'form':form
		}
		return render(self.request, self.template_name, context)



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
			period = form.cleaned_data['period']

			##################################################################
			############          Работает с rabota.ua          ##############
			##################################################################

			# если "все регионы" - то заместт город должно быть "украина"
			if city == 'все регионы':
				city = 'украина'

			if request.user.is_authenticated:
				job = self.model.objects.create(job = job, city = city, site = site, user = user)
				job.save()
				
			slug = City.objects.values_list('slug', flat=True).get(title = city)
			number_id = City.objects.values_list('number_id', flat=True).get(title = city)

			if Job.objects.filter(job=job, city=city, site=site).exists():
				Job.objects.filter(job=job, city=city, site=site).delete()
			count_t, sc = main_script(str(job), city, site, number_id)

			if sc != None:
				[ Job.objects.create(job=job, city=city, site=site, title=i['title'], url=i['url'], 
					description=i['descript'], company=i['company'], date=i['date']) for i in sc ]
			if period == 0:
				data = Job.objects.filter(job=job, city=city, site=site, 
										  date__icontains = 'Сегодня')
				count_t = data.count
			elif period == 1:
				data = Job.objects.filter(Q(date__icontains = 'Сегодня')|Q(date__icontains = 'дн'),
											job=job, city=city, site=site)										  
				count_t = data.count
			elif period == 2:
				data = Job.objects.filter(Q(date__icontains = 'Сегодня')|Q(date__icontains = 'дн')|Q(date__icontains = '1 нед'),
											job=job, city=city, site=site)										  
				count_t = data.count
			else:
				data = Job.objects.filter(job=job, city=city, site=site)

			
			return render(self.request, self.template_name, context = {'form':form, 'data': data, 'count_t':count_t})
		context = {
			'form':form
		}
		return render(self.request, self.template_name, context)



