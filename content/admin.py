from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from .models import Cinema


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin, AdminVideoMixin):
    list_display  = ('name', 'image', 'description', 'program_phone',
                     'reservations_phone', 'admin_phone',
                     'address', 'email', 'opening_hours',
                     'halls_count', 'google_maps_embed')

    search_fields = ('name', 'address')
