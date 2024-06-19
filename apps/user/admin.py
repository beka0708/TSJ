from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import redirect
from django.urls import path
from .models import PasswordReset
from unfold.admin import ModelAdmin
from apps.home.models import FlatOwner, FlatTenant
from unfold.contrib.inlines.admin import TabularInline
from django.utils.translation import gettext_lazy as _

CustomUser = get_user_model()

admin.site.register(PasswordReset)


class TabularOwner(TabularInline):
    model = FlatOwner
    extra = 0
    verbose_name_plural = "Владелец"
    fields = ('tsj', 'flat',)
    classes = ['collapse']

    def get_form_queryset(self, obj):
        """
        Gets all nonrelated objects needed for inlines. Method must be implemented.
        """
        return self.model.objects.all()

    def save_new_instance(self, parent, instance):
        """
        Extra save method which can for example update inline instances based on current
        main model object. Method must be implemented.
        """
        pass


class TabularTenant(TabularInline):
    model = FlatTenant
    extra = 0
    classes = ['collapse']
    def get_form_queryset(self, obj):
        """
        Gets all nonrelated objects needed for inlines. Method must be implemented.
        """
        return self.model.objects.all()

    def save_new_instance(self, parent, instance):
        """
        Extra save method which can for example update inline instances based on current
        main model object. Method must be implemented.
        """
        pass


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    actions_row = []
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
        (_("Общая информация"), {"classes": ["tab"], "fields": ("name", "email", "address", "phone_number")}),

        (_("Одобрение"), {"classes": ["tab"], "fields": ("role", "is_status")}),

    )
    inlines = [TabularOwner, TabularTenant]

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
