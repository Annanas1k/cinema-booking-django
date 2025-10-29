# halls/admin.py
from django.contrib import admin
from .models import Hall, Seat

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    readonly_fields = ('row', 'column', 'seat_type')

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'total_rows', 'total_columns', 'is_3d', 'is_vip')
    list_filter = ('is_3d', 'is_vip')
    search_fields = ('name',)
    inlines = [SeatInline]

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('hall', 'row', 'column', 'seat_type', 'is_functional')
    list_filter = ('hall__name', 'seat_type', 'is_functional')
    search_fields = ('hall__name',)
    list_select_related = ('hall',)