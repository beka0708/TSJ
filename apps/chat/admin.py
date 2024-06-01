from django.contrib import admin

from .models import Message, Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'is_archived', 'has_voting')
    list_filter = ('is_archived', 'has_voting')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    actions = ['archive_rooms', 'unarchive_rooms']

    def archive_rooms(self, request, queryset):
        queryset.update(is_archived=True)
    archive_rooms.short_description = "Archive selected rooms"

    def unarchive_rooms(self, request, queryset):
        queryset.update(is_archived=False)
    unarchive_rooms.short_description = "Unarchive selected rooms"


admin.site.register(Room, RoomAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'room', 'timestamp')
    list_filter = ('room', 'timestamp')
    search_fields = ('content', 'user__name')  # Поиск по содержимому сообщения и имени пользователя


admin.site.register(Message, MessageAdmin)
