from django.urls import path, reverse_lazy
from django.views.generic import CreateView  
from  .import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_views, name='login'),
    path('logout/', views.logout_views, name='logout'),
    path('register/', views.RegistrerViews.as_view(), name='register'), 
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_views, name='change_password'),
    path('users/', views.user_list_view, name='user_list'),  
    path('users/<int:user_id>/toggle_status/', views.toggle_user_status, name='toggle_user_status'), 
    path('users/<int:user_id>/assign-role/', views.assign_role, name='assign_role'),
    path('users/<int:user_id>/validate/', views.validate_user, name='validate_user'), 
    
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/verify/', views.password_reset_verify, name='password_reset_verify'),
    path('password-reset/new/', views.password_reset_new_password, name='password_reset_new_password'),
]

