
from django.urls import path
from .views import fetch_from_github_view, cluster_users_view

urlpatterns = [

    path('fetch-from-github', fetch_from_github_view, name='fetch-from-github'),
    path('cluster-users', cluster_users_view, name='cluster-users'),
    
]
