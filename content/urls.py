# content/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('cinemas/', views.cinema_list, name='cinema_list'),

]