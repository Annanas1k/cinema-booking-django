from django.db import models


class Cinema(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cinemas/', blank=True, null=True)
    description = models.TextField()
    program_phone = models.CharField(max_length=50)
    reservations_phone = models.CharField(max_length=100)
    admin_phone = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    opening_hours = models.CharField(max_length=100, default="Daily, 10:00 - 23:00")
    halls_count = models.IntegerField(default=3)
    google_maps_embed = models.TextField(help_text="Google Maps iframe code")

    def __str__(self):
        return self.name

