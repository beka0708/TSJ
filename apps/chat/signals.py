from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from apps.notifications.models import Notification, ToAdminNotification
from .models import Room, User
from itertools import chain


@receiver(post_save, sender=Room)
def room_create(sender, instance, created, **kwargs):
    if created:
        user_owner_list = User.get_users_by_tsj(tsj_id=instance.tsj.id)
        user_tenant_list = User.get_tenant_users(tsj_id=instance.tsj.id, flattenant__access_to_chats=True)
        users_list = list(chain(user_tenant_list, user_owner_list))
        print(user_tenant_list)
        instance.participants.add(*[user.id for user in users_list])
        # message = f'Новое объявление: {instance.title}'
        # ToAdminNotification.objects.create(
        #     from_user=instance.from_user,
        #     message=message,
        #     link_to=f"/admin/chat/room/{instance.id}/change/"
        # )
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     'notifications',
        #     {
        #         'type': 'send_notification',
        #         'message': message
        #     }
        # )
