from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', getRoutes, name='get_routes'),
    path('projects/', getProjects, name='get_projects'),
    path('projects/<str:pk>/', getProject, name='get_project'),
    path('projects/<str:pk>/vote/', projectVote, name='get_vote'),
]