# movies/admin.py
from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from .models import Movie, ShowTime

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin, AdminVideoMixin):
    list_display = ('title','slug', 'genre', 'duration', 'age_rating', 'release_date', 'language', 'poster')
    list_filter = ('genre', 'language', 'age_rating', 'release_date')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-release_date',)
    pass

@admin.register(ShowTime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'start_time', 'end_time', 'price', 'is_active')
    list_filter = ('hall', 'start_time', 'is_active')
    search_fields = ('movie__title', 'hall__name')
    ordering = ('start_time',)
    list_editable = ('is_active',)