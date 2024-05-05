from django.contrib import admin
from .models import MyDetails, Request

admin.site.register(MyDetails)


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('name_owner', 'tsj', 'number_flat', 'name', 'email', 'number_phone', 'created_date', 'status')
    search_fields = (
        'name_owner__user__name', 'tsj__name', 'number_flat__house__name_block', 'name', 'email', 'number_phone')
    list_filter = ('tsj', 'status')
    readonly_fields = ('created_date',)

