# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Importul corect
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('phone',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        for fieldset in fieldsets:
            if fieldset[0] == 'Personal info':
                fieldset[1]['fields'] = fieldset[1]['fields'] + ('phone',)
                break

        return fieldsets

admin.site.register(User, CustomUserAdmin)