from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import redirect
from django.urls import path, reverse
# from .models import CustomUser
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('phone_number', 'name', 'email',  'is_staff', 'role', 'is_active', 'is_approved')
    ordering = ('name',)
    list_filter = ('is_approved', 'is_active')
    fieldsets = (
        (None, {'fields': ('name', 'email', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Custom fields', {'fields': ('role', 'is_approved')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'phone_number', 'email', 'address', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ('name', 'email', 'phone_number')


admin.site.register(CustomUser, CustomUserAdmin)





