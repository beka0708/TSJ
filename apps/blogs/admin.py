from django.contrib import admin
from .models import News, NewsView


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
