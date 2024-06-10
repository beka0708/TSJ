from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import FlatOwner, FlatTenant, ApartmentHistory, Vote, RequestVoteNews
from apps.chat.models import Room


@receiver(post_save, sender=RequestVoteNews)
def create_vote(sender, instance, created, **kwargs):
    if not created:

        if instance.status == "approved":
            Vote.objects.create(
                tjs_id=instance.tsj_id,
                title=instance.title,
                description=instance.description,
                deadline=instance.deadline_date
            )

@receiver(post_save, sender=Vote)
def create_room_for_vote(sender, instance, created, **kwargs):
    if created:
        room, _ = Room.objects.get_or_create(
            title=instance.title,
            defaults={
                'description': f"Канал для обсуждения голосования '{instance.title}'",
                'has_voting': True
            }
        )
        instance.room = room
        instance.save()


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
