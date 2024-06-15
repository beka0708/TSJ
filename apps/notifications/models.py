from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseNotificationModel(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Notification(BaseNotificationModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Notification for {self.user.phone_number}: {self.message}'


class ToAdminNotification(BaseNotificationModel):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    link_to = models.CharField(max_length=255, null=True, blank=True)
