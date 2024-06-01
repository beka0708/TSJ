from django.contrib import admin

from .models import DomKom, HelpInfo, Camera, \
     Debt, Payment, Photo

admin.site.register(Camera)
admin.site.register(Payment)
admin.site.register(Debt)


class DomKomPhotoInline(admin.TabularInline):
    model = Photo
    extra = 1  # Количество дополнительных пустых форм для загрузки новых фото


@admin.register(DomKom)
class DomKomAdmin(admin.ModelAdmin):
    inlines = [DomKomPhotoInline]


@admin.register(HelpInfo)
class HelpInfoAdmin(admin.ModelAdmin):
    list_display = ("tsj", "title", "url", "number")
    search_fields = ("tsj__name", "title", "url")
