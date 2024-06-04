from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Создаем или обновляем профиль, если пользователь активен и одобрен
    if instance.is_active and instance.is_approved:
        Profile.objects.update_or_create(user=instance)

