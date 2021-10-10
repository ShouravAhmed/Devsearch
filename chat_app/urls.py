from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:pk>/', views.chatapp, name='chatapp'),
    path('inbox/', views.inbox, name='inbox'),
]