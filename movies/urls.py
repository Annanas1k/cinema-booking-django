# movies/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('movies/', views.movie_list_view, name='movie_list'),
    path('allmovies/', views.all_movies_view, name='all_movies'),
    path('movies/<int:movie_id>/', views.movie_detail_view, name='movie_detail'),
    path('booking/<int:showtime_id>/', views.booking_view, name='booking'),
]