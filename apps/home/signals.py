from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import FlatOwner, FlatTenant, ApartmentHistory, Vote, RequestVoteNews
from apps.chat.models import Room
from apps.notifications.models import ToAdminNotification, Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save, sender=RequestVoteNews)
def create_vote(sender, instance, created, **kwargs):
    if not created:

        if instance.status == "approved":
            user = instance.user
            user_profile = user.profile
            message = f'Ваш чат было оплубликовано.'
            # Создание записи уведомления в базе данных
            Notification.objects.create(user=user, message=message)
            admin_notification = ToAdminNotification.objects.filter(
                link_to=f"/admin/home/requestvotenews/{instance.id}/change/").first()
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
            Vote.objects.create(
                tjs_id=user_profile.current_tsj_id,
                title=instance.title,
                description=instance.description,
                deadline_id=instance.deadline_id
            )


@receiver(post_save, sender=Vote)
def create_room_for_vote(sender, instance, created, **kwargs):
    if created:
        room = Room.objects.create(
            title=instance.title,
            description=f"Канал для обсуждения голосования '{instance.title}'",
            has_voting=True,
            tsj_id=instance.tjs_id
        )
        instance.room = room
        instance.save()


@receiver(post_save, sender=RequestVoteNews)
def send_news(sender, instance, created, **kwargs):
    if created:
        message = f'Новый чат: {instance.title}'
        ToAdminNotification.objects.create(
            from_user=instance.user,
            message=message,
            link_to=f"/admin/home/requestvotenews/{instance.id}/change/"
        )
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': message
            }
        )


@receiver(post_save, sender=FlatOwner)
def create_owner_history(sender, instance, created, **kwargs):
    if created:
        description = f"Добавлен новый владелец: {instance.user.name}"
        ApartmentHistory.objects.create(
            flat=instance.flat,
            owner=instance,
            change_date=instance.created_date,
            description=description
        )


@receiver(pre_save, sender=FlatOwner)
def update_flat_owner_history(sender, instance, **kwargs):
    try:
        old_instance = FlatOwner.objects.get(pk=instance.pk)
    except FlatOwner.DoesNotExist:
        pass  # Объект создается впервые, нечего обновлять
    else:
        if old_instance.user != instance.user:
            # Владелец изменился, создаем новую запись в истории квартиры
            ApartmentHistory.objects.create(
                flat=instance.flat,
                owner=old_instance,
                change_date=instance.created_date,  # Предполагается, что у FlatOwner есть поле created_date
                description=f"Владелец квартиры сменился с {old_instance.user.name} на {instance.user.name}"
            )


@receiver(post_save, sender=FlatTenant)
def create_tenant_history(sender, instance, created, **kwargs):
    if created:
        description = f"Добавлен новый жилец: {instance.user.name} в квартиру {instance.flat.number}"
        apartment_history = ApartmentHistory.objects.create(
            flat=instance.flat,
            change_date=instance.created_date,
            description=description
        )
        apartment_history.tenant.set([instance])
        if instance.owner:  # Проверяем, что у квартиранта есть владелец
            apartment_history.owner = instance.owner  # Устанавливаем связь с владельцем квартиры
        apartment_history.save()


@receiver(pre_save, sender=FlatTenant)
def update_flat_tenant_history(sender, instance, **kwargs):
    try:
        old_instance = FlatTenant.objects.get(pk=instance.pk)
    except FlatTenant.DoesNotExist:
        pass  # Объект создается впервые, нечего обновлять
    else:
        if old_instance.user != instance.user:
            # Жилец изменился, создаем новую запись в истории квартиры
            apartment_history = ApartmentHistory.objects.create(
                flat=instance.flat,
                change_date=instance.created_date,  # Предполагается, что у FlatTenant есть поле created_date
                description=f"Жилец квартиры сменился с {old_instance.user.name} на {instance.user.name}"
            )
            apartment_history.tenant.set([old_instance])
            if instance.owner:  # Проверяем, что у квартиранта есть владелец
                apartment_history.owner = instance.owner  # Устанавливаем связь с владельцем квартиры
            apartment_history.save()
