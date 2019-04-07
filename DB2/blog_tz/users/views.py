from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404

from users.models import Subscriber
from users.forms import RegistrationForm, LoginForm, UserUpdateForm, GeneralDescUpdate
from django.views import View
from django.contrib.auth import authenticate, login, get_user_model

from django.contrib import messages

from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from bootstrap_modal_forms.generic import (BSModalUpdateView, BSModalDeleteView)
from django.urls import reverse_lazy


##########################################################################################################
######################           LOGIN / REGISTRATION                #####################################
##########################################################################################################



User = get_user_model()


class RegistrationView(View):
	template_name = 'users/registration.html'
	form = RegistrationForm
	message_send = 'You have registered account.'

	def get(self, request, *args, **kwargs):
		form = self.form
		context = {'form': form}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			new_user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			new_user.set_password(password)
			password_check = form.cleaned_data['password_check']
			new_user.save()
			Subscriber.objects.create(user=User.objects.get(username=new_user.username))

			messages.success(self.request, self.message_send)

			return HttpResponseRedirect('../login')
		context = {'form': form}
		return render(self.request, self.template_name, context)



class LoginView(View):
	template_name = 'users/login.html'
	form = LoginForm
	message_send = 'You are logged in.'

	def get(self, request, *args, **kwargs):
		form = self.form
		context = {'form': form}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			log_user = User.objects.get(email = email)

			user = authenticate(username = log_user.username, password = password)
			if user:
				login(self.request, user)
				messages.success(self.request, self.message_send)
			return HttpResponseRedirect('/')
		context = {'form': form}
		return render(self.request, self.template_name, context)



##########################################################################################################
######################        PROFILE - Detail/Create/Update/Delete         ##############################
##########################################################################################################


class Profile( DetailView):

	model = get_user_model()
	template_name = 'users/profile.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Profile, self).get_context_data(*args, **kwargs)
		context['subscriber'] = Subscriber.objects.get(user__id=self.kwargs.get('pk'))

		# для правильного отображения в шапке имени юзера и правильного перехода по мудакам
		context['user'] = self.request.user
		return context






class ProfileDeleteView(BSModalDeleteView):
    model = User
    template_name = 'users/actions/profile-delete.html'
    success_message = 'Success: Profile was deleted.'
    success_url = reverse_lazy('posts:base-view')


#
# class ProfileUpdateView(View):
#     template_name = 'users/actions/profile-update.html'
#     model = Subscriber
#
#     def get(self, request, **kwargs):
#         pk = self.kwargs.get('pk')
#         sub = get_object_or_404(self.model, pk=pk)
#         uss = User.objects.get(username=sub)
#
#         u_form = UserUpdateForm(instance=uss)
#         p_form = ProfileUpdateForm(instance=sub)
#
#         self.request.session['report_url'] = self.request.META.get('HTTP_REFERER')
#         return render(request, self.template_name, context={'p_form':p_form, 'u_form':u_form})
#
#     def post(self, request, **kwargs):
#         pk = self.kwargs.get('pk')
#         sub = get_object_or_404(self.model, pk=pk)
#         uss = User.objects.get(username=sub)
#
#         u_form = UserUpdateForm(request.POST, instance=uss)
#         p_form = ProfileUpdateForm(request.POST, request.FILES, instance=sub)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(self.request, 'Profile was updated')
#             return HttpResponseRedirect(self.request.session.get('report_url'))
#
#         u_form = UserUpdateForm(instance=uss)
#         p_form = ProfileUpdateForm(instance=sub)
#         return render(request, self.template_name, context={'p_form': p_form, 'u_form':u_form})


######################################################################################
######################################################################################

class GeneralUpdateView(BSModalUpdateView):
    model = Subscriber
    template_name = 'users/actions/profile-update2.html'
    form_class = GeneralDescUpdate
    success_message = 'Success: Subscriber was updated.'

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')




class PersonalUpdateView(BSModalUpdateView):
    model = User
    template_name = 'users/actions/profile-update2.html'
    form_class = UserUpdateForm
    success_message = 'Success: Personal Info was updated.'

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')
