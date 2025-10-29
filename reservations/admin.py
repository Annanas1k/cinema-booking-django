# reservations/admin.py
from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'showtime', 'seat', 'status', 'reserved_at', 'paid_at')
    list_filter = ('status', 'showtime', 'reserved_at')
    search_fields = ('user__username', 'payment_ref')
    fieldsets = (
        (None, {'fields': ('user', 'showtime', 'seat', 'status')}),
        ('Detalii Plată', {'fields': ('payment_ref', 'paid_at')}),
        ('Timpi', {'fields': ('reserved_at',)}),
    )
    readonly_fields = ('reserved_at',)