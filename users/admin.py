# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Importul corect
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('phone',)

    fieldsets = UserAdmin.fieldsets + (
        ('Contact Information', {'fields': ('phone',)}),
    )

admin.site.register(User, CustomUserAdmin)