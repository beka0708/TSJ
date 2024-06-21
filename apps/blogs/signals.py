from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.notifications.models import Notification, ToAdminNotification
from .models import News


@receiver(post_save, sender=News)
def send_notification_on_approve_news(sender, instance, created, **kwargs):
    if not created:
        if instance.is_approve == 'approved':
            user = instance.from_user
            profile_user = user.profile
            message = f'Ваше обьявление было оплубликовано.'
            # Создание записи уведомления в базе данных
            Notification.objects.create(user=user, message=message)
            admin_notification = ToAdminNotification.objects.filter(
                link_to=f"/admin/blogs/news/{instance.id}/change/").first()
            if admin_notification:
                admin_notification.read = True
                admin_notification.save()
            # Отправка уведомления по WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'notifications_{user.id}',
                {
                    'type': 'send_notification',
                    'message': message,
                }
            )


@receiver(post_save, sender=News)
def send_news(sender, instance, created, **kwargs):
    if created:
        message = f'Новое объявление: {instance.title}'
        ToAdminNotification.objects.create(
            from_user=instance.from_user,
            message=message,
            link_to=f"/admin/blogs/news/{instance.id}/change/"
        )
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': message
            }
        )
