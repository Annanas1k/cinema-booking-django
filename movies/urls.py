# movies/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('filme/', views.movie_list_view, name='movie_list'),
]