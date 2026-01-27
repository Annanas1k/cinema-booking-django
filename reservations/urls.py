from django.urls import path
from . import views

urlpatterns = [
    path('<int:hall_id>/booking/<int:showtime_id>/', views.booking_view, name='booking_screen'),
    path('booking/success/<int:showtime_id>/', views.booking_success_view, name='booking_success'),
]