from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Room(models.Model):
    title = models.CharField(max_length=255, null=True, verbose_name="Название канала")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата создания")
    is_archived = models.BooleanField(default=False, verbose_name="Архивировать чат")
    has_voting = models.BooleanField(default=False, null=True, verbose_name="Голосование")
    is_discussion = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    def get_url(self):
        return f"/chat/{self.id}/"

    def __str__(self):
        return self.title


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE, verbose_name="Канал")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='username', verbose_name="Пользователь")
    content = models.TextField(verbose_name="Сообщение")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        ordering = ['timestamp']
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.user.name + ": " + self.content
