from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import (
    TSJ,
    House,
    FlatOwner,
    FlatTenant,
    Flat,
    News,
    Vote,
    Request_Vote_News,
    ApartmentHistory,
    ViewRecord  # Добавляем новую модель
)

User = get_user_model()


class FlatOwnerInline(admin.TabularInline):
    model = FlatOwner
    extra = 1


class FlatInline(admin.TabularInline):
    model = FlatTenant
    extra = 1


@admin.register(TSJ)
class TSJAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = (
        "name_block",
        "address",
        "geo_position",
        "floors",
        "entrances",
        "flats_number",
    )
    search_fields = ("name_block", "address")
    ordering = ("name_block",)


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "house",
    )
    search_fields = ("house__name_block", "number")
    ordering = (
        "house",
        "number",
    )
    list_filter = ("house",)
    raw_id_fields = ("house",)
    inlines = [FlatOwnerInline]


@admin.register(FlatTenant)
class FlatTenantAdmin(admin.ModelAdmin):
    list_display = ("user", "flat")
    search_fields = ("user__username",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("tsj", "type", "title", "created_date", "update_date", "view_count")
    search_fields = ("tsj__name", "title")
    list_filter = ("tsj", "type")
    readonly_fields = ("created_date", "update_date", "view_count")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("title", "created_date", "deadline", "view_count")
    search_fields = ("title",)
    list_filter = ("tjs",)
    readonly_fields = ("created_date", "view_count")


@admin.register(Request_Vote_News)
class RequestVoteAdmin(admin.ModelAdmin):
    list_display = ("title", "created_date")


class ApartmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('flat', 'owner', 'get_tenant_names', 'change_date', 'description')
    list_filter = ('flat', 'owner', 'change_date')
    search_fields = ('description', 'flat__number', 'owner__user__name', 'tenant__user__name')

    def get_tenant_names(self, obj):
        return ", ".join([tenant.user.name for tenant in obj.tenant.all()])
    get_tenant_names.short_description = 'Tenants'


admin.site.register(ApartmentHistory, ApartmentHistoryAdmin)


@admin.register(ViewRecord)
class ViewRecordAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'content_type', 'viewed_at')
    list_filter = ('content_type', 'viewed_at')
    search_fields = ('user__name', 'content_type', 'content_id')

    def get_user(self, obj):
        return obj.user.name
    get_user.short_description = 'Пользователь'
