from django.contrib import admin
from .models import News, NewsView
from unfold.admin import ModelAdmin
from unfold.contrib.inlines.admin import NonrelatedTabularInline


class NewsViewInline(NonrelatedTabularInline):
    model = NewsView
    extra = 0

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


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ("tsj", "type", "title", "created_date", "update_date", "views_count")
    search_fields = ("tsj__name", "title")
    list_filter = ("tsj", "type")
    readonly_fields = ("created_date", "update_date")
    inlines = [NewsViewInline]

    def views_count(self, obj):
        return obj.views.count()

    views_count.short_description = "Просмотры"


admin.site.register(NewsView)
