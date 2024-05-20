from django.contrib import admin
from .models import DomKom, HelpInfo, Camera, \
    PaymentType, Debt, Payment

admin.site.register(DomKom)
admin.site.register(Camera)
admin.site.register(Payment)
admin.site.register(PaymentType)
admin.site.register(Debt)


@admin.register(HelpInfo)
class HelpInfoAdmin(admin.ModelAdmin):
    list_display = ("tsj", "title", "url", "number")
    search_fields = ("tsj__name", "title", "url")