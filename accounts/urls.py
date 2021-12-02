from django.urls import path

from .views import (RegistrationView, LogInView, LogOutView, UserCreationView, UserDetailView,
                    WorkerCreationView, WorkerDetailView, WorkerListView, UserListView, UserChangePasswordView)

app_name = 'accounts'


urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),

    path('user-list/', UserListView.as_view(), name='user_list'),
    path('user-creation/', UserCreationView.as_view(), name='user_creation'),
    path('user-detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user-change-password/<int:pk>/', UserChangePasswordView.as_view(), name='user_change_password'),

    path('worker-list/', WorkerListView.as_view(), name='worker_list'),
    path('worker-creation/', WorkerCreationView.as_view(), name='worker_creation'),
    path('worker-detail/<int:pk>/', WorkerDetailView.as_view(), name='worker_detail'),
]
