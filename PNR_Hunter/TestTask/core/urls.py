from django.urls import path

from .views import (LoginView, RegistrationView,
	ProjectCreateListView, ProjectListView,
	MainUpdate,
	ProjectDelete, TaskDelete, DeleteAllTasks,)

# for logout
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView




urlpatterns = [
	path('', ProjectCreateListView.as_view(), name ='base-view'),
	path('project/<int:pk>-<str:title>/', ProjectListView.as_view(), name = 'project-detail'),

	# update
	path('update/<int:pk>-<str:title>', MainUpdate.as_view(), name = 'update'),

	# delete
	path('delete/project/<pk>-<title>', ProjectDelete.as_view(), name = 'project-delete'),
	path('delete/task/<pk>-<title>', TaskDelete.as_view(), name = 'task-delete'),
	path('delete-all-tasks/', DeleteAllTasks.as_view(), name = 'delete-all-tasks'),

    # user
    path('logout/', LogoutView.as_view(next_page = reverse_lazy('base-view')), name ='logout-view'),
    path('login/', LoginView.as_view(), name ='login-view'),
    path('registration/', RegistrationView.as_view(), name = 'registration-view'),
]

