from django.contrib import admin
from .models import DomKom, HelpInfo, Receipts, YourForms, Camera

admin.site.register(DomKom)
admin.site.register(Receipts)
admin.site.register(YourForms)
admin.site.register(Camera)


@admin.register(HelpInfo)
class HelpInfoAdmin(admin.ModelAdmin):
    list_display = ("tsj", "title", "url", "number")
    search_fields = ("tsj__name", "title", "url")