from django.contrib import admin
from .models import ToAdminNotification
from unfold.admin import ModelAdmin


@admin.register(ToAdminNotification)
class NewsAdmin(ModelAdmin):
    pass
