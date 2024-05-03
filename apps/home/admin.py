from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import TSJ, House, FlatOwner, FlatTenant, Flat, News, Request, HelpInfo, Vote
from .models import *

User = get_user_model()


class FlatOwnerInline(admin.TabularInline):
    model = FlatOwner
    extra = 1


class FlatInline(admin.TabularInline):
    model = FlatTenant
    extra = 1


@admin.register(TSJ)
class TSJAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('name_block', 'address', 'geo_position', 'floors', 'entrances', 'flats_number')
    search_fields = ('name_block', 'address')


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    list_display = ('house', 'number')
    search_fields = ('house__name_block', 'number')
    inlines = [FlatOwnerInline]


@admin.register(FlatTenant)
class FlatTenantAdmin(admin.ModelAdmin):
    list_display = ('user', 'flat')
    search_fields = ('user__username',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('tsj', 'type', 'title', 'created_date', 'update_date')
    search_fields = ('tsj__name', 'title')
    list_filter = ('tsj', 'type')
    readonly_fields = ('created_date', 'update_date')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('name_owner', 'tsj', 'number_flat', 'name', 'email', 'number_phone', 'created_date', 'status')
    search_fields = (
        'name_owner__user__name', 'tsj__name', 'number_flat__house__name_block', 'name', 'email', 'number_phone')
    list_filter = ('tsj', 'status')
    readonly_fields = ('created_date',)


@admin.register(HelpInfo)
class HelpInfoAdmin(admin.ModelAdmin):
    list_display = ('tsj', 'title', 'url', 'number')
    search_fields = ('tsj__name', 'title', 'url')


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('tsj', 'title', 'vote_type', 'created_date', 'end_date')
    search_fields = ('tsj__name', 'title', 'vote_type')
    list_filter = ('tsj', 'vote_type')
    readonly_fields = ('created_date', 'end_date')


admin.site.register(VoteNew)
# admin.site.register(VoteRecord)
