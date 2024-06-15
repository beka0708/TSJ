from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.notifications.models import Notification, ToAdminNotification
from .models import Room


@receiver(post_save, sender=Room)
def send_news(sender, instance, created, **kwargs):
    if created:
        message = f'Новое объявление: {instance.title}'
        ToAdminNotification.objects.create(
            from_user=instance.from_user,
            message=message,
            link_to=f"/admin/chat/room/{instance.id}/change/"
        )
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': message
            }
        )
