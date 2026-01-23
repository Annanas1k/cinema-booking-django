from django.urls import path
from . import views

urlpatterns = [
    # Ruta va fi: /reservation/booking/5/ (unde 5 este ID-ul ShowTime-ului)
    path('<int:hall_id>/booking/<int:showtime_id>/', views.booking_view, name='booking_screen'),
]