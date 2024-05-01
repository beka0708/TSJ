from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.user.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    OWNER = 'OWNER'
    TENANT = 'TENANT'
    MANAGER = 'MANAGER'
    LODGER = 'LODGER'
    ROLE_CHOICES = [
        (OWNER, 'Владелец'),
        (TENANT, 'Арендатор'),
        (MANAGER, 'Менеджер'),
        (LODGER, 'Жилец'),
    ]

    APPROVED = 'APPROVED'
    NOT_APPROVED = 'NOT_APPROVED'
    PENDING = 'PENDING'
    APPROVAL_CHOICES = [
        (APPROVED, 'Одобрен'),
        (NOT_APPROVED, 'Не одобрен'),
        (PENDING, 'В ожидании'),
    ]

    DoesNotExist = None
    phone_number = PhoneNumberField('Номер телефона', region='KG', unique=True,
                                    help_text='Пример: +996700777777', null=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, verbose_name="Имя", )
    address = models.CharField(max_length=255, verbose_name="Адрес", )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True,
                            default=LODGER, verbose_name="Роль")

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_approved = models.CharField(max_length=12, choices=APPROVAL_CHOICES,
                                   default=PENDING, null=True, verbose_name="Одобрение")

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if self.is_approved == CustomUser.APPROVED:
            self.is_active = True
        else:
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"
