from django.urls import path

from . import views

urlpatterns = [
    path('projects/', views.projects, name='project_list'),
    path('project/<str:pk>/', views.project, name='project'),
    path('projects/create/', views.create_project, name='create_project'),
    path('project/<str:pk>/update/', views.update_project, name='update_project'),
    path('project/<str:pk>/delete/', views.delete_project, name='delete_project'),
]
