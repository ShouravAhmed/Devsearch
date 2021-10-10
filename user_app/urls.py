from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('varify_account/', views.varify_account, name='varify_account'),
    path('varify_account_success/<str:pk>/', views.varify_account_success, name='varify_account_success'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='user_app/reset_password.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='user_app/reset_password_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='user_app/reset.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user_app/reset_password_complete.html'), name='password_reset_complete'),

    path('profile/<str:pk>/update/', views.update_profile, name='update_profile'),
    path('skill/create/', views.create_skill, name='create_skill'),
    path('skill/<str:pk>/update/', views.update_skill, name='update_skill'),
    path('skill/<str:pk>/delete/', views.delete_skill, name='delete_skill'),
]
