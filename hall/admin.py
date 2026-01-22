# halls/admin.py
from django.contrib import admin
from .models import Hall, Seat

class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    readonly_fields = ('row', 'column')

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('name', 'cinema', 'capacity', 'total_rows', 'total_columns', 'is_3d')
    list_filter = ('is_3d', 'capacity')
    search_fields = ('name',)
    readonly_fields = ('capacity',)
    inlines = [SeatInline]

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('hall', 'row', 'column', 'is_functional')
    list_filter = ('hall__name', 'is_functional')
    search_fields = ('hall__name',)
    list_select_related = ('hall',)