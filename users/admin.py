# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # Importul corect
from .models import User


# Extindem clasa UserAdmin pentru a include câmpul nostru custom 'phone'.
class CustomUserAdmin(UserAdmin):
    # Adaugă 'phone' la lista de câmpuri afișate în lista de utilizatori
    list_display = UserAdmin.list_display + ('phone',)

    # Adaugă 'phone' în seturile de câmpuri editabile în pagina de detalii
    fieldsets = UserAdmin.fieldsets + (
        ('Informații Contact', {'fields': ('phone',)}),
    )


# Înregistrează modelul cu clasa custom de administrare
admin.site.register(User, CustomUserAdmin)