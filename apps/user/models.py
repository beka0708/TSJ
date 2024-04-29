from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from apps.user.managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractBaseUser, PermissionsMixin):
    OWNER = 'OWNER'
    TENANT = 'TENANT'
    MANAGER = 'MANAGER'
    ROLE_CHOICES = [
        (OWNER, 'Владелец'),
        (TENANT, 'Арендатор'),
        (MANAGER, 'Менеджер'),
    ]

    DoesNotExist = None
    phone_number = PhoneNumberField('Номер телефона', region='KG', unique=True,
                                    help_text='Пример: +996700777777', null=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, verbose_name="Имя",)
    address = models.CharField(max_length=255, verbose_name="Адрес",)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True,
                            verbose_name="Роль")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"
