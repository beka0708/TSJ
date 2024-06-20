from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import (
    TSJ,
    House,
    FlatOwner,
    FlatTenant,
    Flat,
    Vote,
    RequestVoteNews,
    ApartmentHistory,
    VoteResult,
    VoteView,
    DomKomRole,
    HouseDeveloper,
    HousePhoto,
    DeadLine
)

User = get_user_model()


@admin.register(DeadLine)
class TSJAdmin(ModelAdmin):
    pass


class FlatOwnerInline(admin.TabularInline):
    model = FlatOwner
    extra = 1


admin.site.register(FlatOwner)
admin.site.register(DomKomRole)
admin.site.register(HouseDeveloper)
admin.site.register(HousePhoto)


class FlatInline(admin.TabularInline):
    model = Flat
    fields = ('number', 'get_owner',)
    readonly_fields = ('number', 'get_owner',)
    extra = 1


@admin.register(TSJ)
class TSJAdmin(ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(House)
class HouseAdmin(ModelAdmin):
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
    inlines = (FlatInline,)


@admin.register(Flat)
class FlatAdmin(ModelAdmin):
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
class FlatTenantAdmin(ModelAdmin):
    list_display = ("user", "flat")
    search_fields = ("user__username",)


class VoteResultInline(admin.TabularInline):
    model = VoteResult
    extra = 0


@admin.register(Vote)
class VoteAdmin(ModelAdmin):
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
class VoteViewAdmin(ModelAdmin):
    list_display = ('vote', 'user', 'viewed_at')  # Поля для отображения в списке
    list_filter = ('vote', 'user')  # Фильтры для списка
    search_fields = ('vote__title', 'user__username')  # Поиск по заголовку голосования и имени пользователя
    ordering = ['viewed_at']  # Сортировка по времени просмотра

    def viewed_at(self, obj):  # Пользовательское поле для отображения времени просмотра
        return obj.viewed_at.strftime('%Y-%m-%d %H:%M:%S')

    viewed_at.short_description = 'Время просмотра'


@admin.register(RequestVoteNews)
class RequestVoteAdmin(ModelAdmin):
    list_display = ("title", "created_date")


class ApartmentHistoryAdmin(ModelAdmin):
    list_display = ('flat', 'owner', 'get_tenant_names', 'change_date', 'description')
    list_filter = ('flat', 'owner', 'change_date')
    search_fields = ('description', 'flat__number', 'owner__user__name', 'tenant__user__name')

    def get_tenant_names(self, obj):
        return ", ".join([tenant.user.name for tenant in obj.tenant.all()])

    get_tenant_names.short_description = 'Tenants'


admin.site.register(ApartmentHistory, ApartmentHistoryAdmin)
