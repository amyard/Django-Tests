from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Project, Task
from .forms import ProjectForm, TaskForm, ProjectFormUpdate, TaskFormUpdate
from .mixins import *
from django.core.paginator import Paginator
from django.db.models import Count

from user.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, get_user_model
from django.views import View
from user.models import UserAccount


#########################################################################################
##################################        USERS       ###################################
#########################################################################################

User = get_user_model()

class LoginView(View):
	template_name = 'users/login.html'
	form = LoginForm

	def get(self, request, *args, **kwargs):
		form = self.form
		context = {'form': form}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username = username, password = password)
			if user:
				login(self.request, user)
			return HttpResponseRedirect('/')
		context = {'form': form}
		return render(self.request, self.template_name, context)



class RegistrationView(View):
	template_name = 'users/registration.html'
	form = RegistrationForm

	def get(self, request,*args,**kwargs):
		form = self.form
		context = {'form':form}
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
			UserAccount.objects.create(user = User.objects.get(username=new_user.username))
			return HttpResponseRedirect('../login')
		context = {'form':form}
		return render(self.request, self.template_name, context)



#########################################################################################
##################################        Category    ###################################
#########################################################################################

class ProjectCreateListView(View, CreateMixin):
	model = Project
	model2 = Task
	template_name = 'core/main.html'
	title = 'Main page'
	paginate_by = 5
	form = ProjectForm
	form2 = TaskForm
	redirect_path = '/'


	def get_queryset(self):
		return self.model2.objects.filter(project__user__username = self.request.user)



#########################################################################################
##########################        DETAIL OF CATEGORY       ##############################
#########################################################################################

class ProjectListView(ProjectCreateListView, View):
	
	def get_queryset(self):
		return self.model2.objects.filter(project__user__username = self.request.user, 
			project_id = self.kwargs.get('pk'))



#########################################################################################
##########################              SEARCH             ##############################
#########################################################################################

class SearchView(ProjectCreateListView, View):
	paginate_by = 30
	
	def get_queryset(self):
		query = self.request.GET.get('q')
		return self.model2.objects.filter(Q(project__title__icontains = query)|Q(title__icontains = query), project__user__username = self.request.user)




#########################################################################################
##########################              UPDATE             ##############################
#########################################################################################



class MainUpdate(View):
	model = Project
	model2 = Task
	template_name = 'core/main.html'
	title = 'Main page'
	form = ProjectFormUpdate
	form2 = TaskFormUpdate
	redirect_path = '/'
	detail = None
	paginate_by = 5


	def get_queryset(self):
		return self.model2.objects.filter(project__user__username = self.request.user)


	def get(self, request, **kwargs):
		pk = self.kwargs.get('pk')
		title = self.kwargs.get('title')

		try:
			tag = self.model.objects.get(id = pk)
			tag2 = None
			form = self.form(instance = tag)
			form2 = self.form2
		except:
			tag = None
			tag2 = self.model2.objects.get(id = pk)
			form = self.form
			form2 = self.form2(instance = tag2)
		self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')


		user = self.request.user
		projects = self.model.objects.filter(user__username = user)
		df = self.model2.objects.filter(project__user__username = user)
	
		p = Paginator(df, self.paginate_by)
		page_number = request.GET.get('page')
		page = p.get_page(page_number)

		title = self.title
		count_tasks = self.model.objects.filter(user__username = user).annotate(count=Count('project__title')).values('title', 'count')

		context = {'projects':projects, 'tasks':page, 'title':title, 'form':form, 'form2':form2, 'detail':self.detail, 'count_tasks':count_tasks}
		return render(request, self.template_name, context)


	def post(self, request, **kwargs):
		form = self.form
		form2 = self.form2
		pk = self.kwargs.get('pk')

		if 'form' in request.POST:
			tag = self.model.objects.get(id = pk)
			form = self.form(request.POST, instance = tag, user = self.request.user)
			form2 = self.form2
			if form.is_valid():
				new_tag = form.save()
				return HttpResponseRedirect(self.request.session.get('report_url'))

		elif 'form2' in request.POST:
			tag = self.model2.objects.get(id = pk)
			form = self.form
			form2 = self.form2(request.POST, instance = tag, user = self.request.user)
			if form2.is_valid():
				new_tag = form2.save()
				return HttpResponseRedirect(self.request.session.get('report_url'))
		else:
			return render(self.request, self.template_name, {'form2':form2, 'form':form})

		user = self.request.user
		projects = self.model.objects.filter(user__username = user)
		df = self.get_queryset()
	
		p = Paginator(df, self.paginate_by)
		page_number = request.GET.get('page')
		page = p.get_page(page_number)

		title = self.title
		count_tasks = self.model.objects.filter(user__username = user).annotate(count=Count('project__title')).values('title', 'count')

		context = {'form2':form2, 'form':form, 'tasks':page, 'projects':projects, 'detail': self.detail, 'title':title,'count_tasks':count_tasks}
		
		return render(self.request, self.template_name, context)





#########################################################################################
##################################        DELETE      ###################################
#########################################################################################

class ProjectDelete(DeleteMixin, DeleteView):
	model = Project

class TaskDelete(DeleteMixin, DeleteView):
	model = Task





class DeleteAllTasks(View):
	model2 = Task
	template_name = 'core/main.html'


	def get(self, reguest, **kwargs):
		self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
		return render(self.request, self.request.session['report_url'])

	def get(self, reguest, **kwargs):
		self.model2.objects.filter(project__user__username = self.request.user).delete()
		self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
		return HttpResponseRedirect(self.request.session['report_url'])


class DeleteUser(View):
	model = User
	template_name = 'core/main.html'


	# def get(self, reguest, **kwargs):
	# 	self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
	# 	return render(self.request, self.request.session['report_url'])

	def get(self, reguest, **kwargs):
		self.model.objects.filter(username = self.request.user).delete()
		self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
		return redirect('registration-view')





