from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
import re
from apps.user.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    OWNER = "OWNER"
    TENANT = "TENANT"
    MANAGER = "MANAGER"
    LODGER = "LODGER"
    ROLE_CHOICES = [
        (OWNER, "Владелец"),
        (TENANT, "Арендатор"),
        (MANAGER, "Менеджер"),
        (LODGER, "Жилец"),
    ]

    APPROVED = "APPROVED"
    NOT_APPROVED = "NOT_APPROVED"
    PENDING = "PENDING"
    APPROVAL_CHOICES = [
        (APPROVED, "Одобрен"),
        (NOT_APPROVED, "Не одобрен"),
        (PENDING, "В ожидании"),
    ]

    DoesNotExist = None
    phone_number = PhoneNumberField(
        "Номер телефона",
        region="KG",
        unique=True,
        help_text="Пример: +996700777777",
        null=True,

    )
    # phone_number = models.CharField(max_length=13, verbose_name='Номер телефона', unique=True,
    #                                 help_text='Пример: +996700777777', null=True)
    email = models.EmailField(unique=True)
    name = models.CharField(
        max_length=100,
        verbose_name="Имя",
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Адрес",
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        null=True,
        default=LODGER,
        verbose_name="Роль",
    )
    verification_code = models.CharField(max_length=4, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_status = models.CharField(
        max_length=12,
        choices=APPROVAL_CHOICES,
        default=PENDING,
        null=True,
        verbose_name="Одобрение",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]

    def save(self, *args, **kwargs):
        if self.is_status == CustomUser.APPROVED:
            self.is_active = True
        elif self.is_status == CustomUser.NOT_APPROVED:
            self.is_active = False
        else:
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def clean(self):
        super().clean()
        # Проверяем, что имя содержит только буквы (кириллица и латиница допустимы)
        if not re.match(r'^[а-яА-ЯёЁa-zA-Z\s]+$', self.name):
            raise ValidationError("Имя должно содержать только буквы.")


class DeviceToken(models.Model):
    token = models.CharField(max_length=255)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="devise_token"
    )

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "token-device"
# {
#     "email":
#         "money@gmal.com",
#     "phone_number":
#         "+996700777776",
#     "name":
#         "Lisa ",
#     "password":
#         "money$$$",
#     "confirm_password":
#         "money$$$",
#     "address":
#         "Земля, тоже земля, 1, 1"
# }

# {
#     "phone_number":
#         "+996700777776",
#     "password":
#         "money$$$"
# }
