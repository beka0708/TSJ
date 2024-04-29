from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('name', 'email', 'phone_number', 'is_staff', 'role', 'is_active')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'email', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Custom fields', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone_number', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'role'),
        }),
    )
    search_fields = ('name', 'email', 'phone_number')


admin.site.register(CustomUser, CustomUserAdmin)
