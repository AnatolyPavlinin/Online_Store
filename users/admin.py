from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets[:-1]
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные поля', {'fields': ('avatar', 'phone_number', 'country')}),
    )
