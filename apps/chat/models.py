from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Room(models.Model):
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return self.user.name + ": " + self.content
