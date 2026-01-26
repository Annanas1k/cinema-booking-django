# content/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('cinemas/', views.cinema_list, name='cinema_list'),
    path('news/', views.news_list, name='news_list'),
    path('shop/', views.shop_view, name='shop_view'),
]