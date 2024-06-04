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
    email = models.EmailField(unique=True, blank=True)
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
        # Check current state of the user
        is_new_user = self.pk is None
        old_user = None if is_new_user else CustomUser.objects.get(pk=self.pk)

        # Update is_active status based on is_status
        if self.is_status == CustomUser.APPROVED:
            self.is_active = True
        elif self.is_superuser:
            self.is_active = True
        elif self.is_status == CustomUser.NOT_APPROVED:
            self.is_active = False
        elif self.is_superuser:
            self.is_active = True
        else:
            self.is_active = False

        super().save(*args, **kwargs)

        # Create profile if user is approved and active
        if not is_new_user:
            if old_user.is_active != self.is_active or old_user.is_approved != self.is_approved:
                if self.is_active and self.is_approved:
                    from apps.userprofile.models import Profile
                    Profile.objects.get_or_create(user=self)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        # Проверяем, что имя содержит только буквы (кириллица и латиница допустимы)
        if not re.match(r'^[а-яА-ЯёЁa-zA-Z\s]+$', self.name):
            raise ValidationError("Имя должно содержать только буквы.")

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"


class DeviceToken(models.Model):
    token = models.CharField(max_length=255)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="devise_token"
    )

    def __str__(self):
        return self.user.name

    class Meta:
        verbose_name = "token-device"
