from django.urls import path
from .views import (LoginView, RegistrationView,

					# DetailView
					ProjectListView, SevenDaysListView,

                    # DeleteView
                    ProjectDelete,TaskDelete,

                    # Update
                    TodayUpdate, 
                    Test, 
	)

# for logout
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('', ProjectListView.as_view(), name = 'base_view'),
    path('7days/', SevenDaysListView.as_view(), name = 'task_7today'),

    # delete
    path('delete/project/<pk>', ProjectDelete.as_view(), name = 'project-delete'),
    path('delete/task/<pk>', TaskDelete.as_view(), name = 'task-delete'),

    # update
    path('update-project/<pk>', TodayUpdate.as_view(), name = 'project-update'),

    # projects
    # path('<int:id>', Test.as_view(), name = 'test'),
    path('<pk>-<name>', Test.as_view(), name = 'test'),

    # users
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('base_view')), name = 'logout_view'),
    path('login/', LoginView.as_view(), name = 'login_view'),
    path('registration/', RegistrationView.as_view(), name = 'registration'),


]
