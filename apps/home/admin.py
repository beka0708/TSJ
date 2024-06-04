from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html

from .models import (
    TSJ,
    House,
    FlatOwner,
    FlatTenant,
    Flat,
    News,
    Vote,
    Request_Vote_News, ApartmentHistory, VoteResult, VoteView, NewsView,
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


class NewsViewInline(admin.TabularInline):
    model = NewsView
    extra = 0


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("tsj", "type", "title", "created_date", "update_date", "views_count")
    search_fields = ("tsj__name", "title")
    list_filter = ("tsj", "type")
    readonly_fields = ("created_date", "update_date")
    inlines = [NewsViewInline]

    def views_count(self, obj):
        return obj.views.count()
    views_count.short_description = "Просмотры"


admin.site.register(NewsView)


class VoteResultInline(admin.TabularInline):
    model = VoteResult
    extra = 0


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'tjs', 'created_date', 'deadline', 'yes_count', 'no_count', 'room_link')
    list_filter = ('tjs', 'created_date', 'deadline')
    search_fields = ('title',)

    def room_link(self, obj):
        if obj.room:
            return format_html(f"<a href='{obj.room.get_url()}'>Перейти к каналу</a>")
        return None

    room_link.allow_tags = True
    room_link.short_description = 'Ссылка на канал'


@admin.register(VoteView)
class VoteViewAdmin(admin.ModelAdmin):
    list_display = ('vote', 'user', 'viewed_at')  # Поля для отображения в списке
    list_filter = ('vote', 'user')  # Фильтры для списка
    search_fields = ('vote__title', 'user__username')  # Поиск по заголовку голосования и имени пользователя
    ordering = ['viewed_at']  # Сортировка по времени просмотра

    def viewed_at(self, obj):  # Пользовательское поле для отображения времени просмотра
        return obj.viewed_at.strftime('%Y-%m-%d %H:%M:%S')

    viewed_at.short_description = 'Время просмотра'


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
