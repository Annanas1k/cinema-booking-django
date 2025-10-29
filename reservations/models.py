from django.db import models
from django.conf import settings
from movies.models import ShowTime
from hall.models import Seat

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('reserved', 'Rezervat'),
        ('paid', 'Plătit'),
        ('canceled', 'Anulat')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reserved')
    reserved_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    payment_ref = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('showtime', 'seat')

    def __str__(self):
        return f"{self.user.username} - {self.showtime.movie.title} ({self.showtime.start_time})"