from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import redirect
from django.urls import path
from .models import PasswordReset
from unfold.admin import ModelAdmin
CustomUser = get_user_model()

admin.site.register(PasswordReset)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = (
        "phone_number",
        "name",
        "email",
        "is_staff",
        "role",
        "is_active",
        "is_approved",
        "is_status",
        "verification_code"
    )
    ordering = ("name",)
    list_filter = ("is_status", "is_active")
    search_fields = ("name", "email", "phone_number")

    fieldsets = (
        ("Общая информация", {"fields": ("name", "email", "address", "phone_number")}),

        ("Одобрение", {"fields": ("role", "is_status")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "phone_number",
                    "email",
                    "address",
                    "password1",
                    "password2",
                    "role",
                ),
            },
        ),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "get_user/<int:object_id>/",
                self.admin_site.admin_view(self.get_user),
                name="get_user",
            ),
        ]
        return custom_urls + urls

    def get_user(self, request, object_id):
        user = CustomUser.objects.get(pk=object_id)
        if user.is_status != CustomUser.APPROVED:
            user.is_status = CustomUser.APPROVED
            user.is_active = True
            user.save()
        return redirect("admin:apps_user_changelist")

