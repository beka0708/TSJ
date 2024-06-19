from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import DomKom, HelpInfo, Camera, \
    Debt, Payment, Photo

admin.site.register(Payment)
admin.site.register(Debt)


@admin.register(Camera)
class DomKomAdmin(ModelAdmin):
    pass


class DomKomPhotoInline(TabularInline):
    model = Photo
    extra = 1  # Количество дополнительных пустых форм для загрузки новых фото


@admin.register(DomKom)
class DomKomAdmin(ModelAdmin):
    inlines = [DomKomPhotoInline]


@admin.register(HelpInfo)
class HelpInfoAdmin(ModelAdmin):
    list_display = ("tsj", "title", "url", "number")
    search_fields = ("tsj__name", "title", "url")
