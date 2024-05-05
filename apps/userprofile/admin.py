from django.contrib import admin
from apps.userprofile.models import Request, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = (
        "name_owner",
        "tsj",
        "number_flat",
        "name",
        "email",
        "number_phone",
        "created_date",
        "status",
    )
    search_fields = (
        "name_owner__user__name",
        "tsj__name",
        "number_flat__house__name_block",
        "name",
        "email",
        "number_phone",
    )
    list_filter = ("tsj", "status")
    readonly_fields = ("created_date",)

