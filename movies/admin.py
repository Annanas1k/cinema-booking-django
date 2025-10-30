# movies/admin.py
from django.contrib import admin
from .models import Movie, ShowTime

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'duration', 'age_rating', 'release_date', 'language', 'poster')
    list_filter = ('genre', 'language', 'age_rating', 'release_date')
    search_fields = ('title', 'description')
    ordering = ('-release_date',)

@admin.register(ShowTime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'start_time', 'end_time', 'price', 'is_active')
    list_filter = ('hall', 'start_time', 'is_active')
    search_fields = ('movie__title', 'hall__name')
    ordering = ('start_time',)
    list_editable = ('is_active',)