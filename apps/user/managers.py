from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, phone_number, email, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Поле «Номер телефона» должно быть заполнено.")
        if not email:
            raise ValueError("Поле Электронная почта должно быть установлено")

        extra_fields.setdefault("is_approved", False)
        extra_fields.setdefault("is_active", False)

        user = self.model(
            phone_number=phone_number, email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_approved", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # is_superuser = extra_fields.pop('is_superuser', False)

        # Создание пользователя с помощью create_user и установление is_superuser вручную
        user = self.create_user(phone_number, email, password, **extra_fields)
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
