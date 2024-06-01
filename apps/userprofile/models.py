from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.home.models import FlatOwner, TSJ, Flat

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',
                                verbose_name="Пользователь", help_text="Чей профиль")
    cover = models.ImageField(upload_to='avatars/', null=True, blank=True,
                              verbose_name="Фото", default='avatars/default_avatar')

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        email = self.user.email if self.user.email else "Нет email"
        address = self.user.address if self.user.address else "Нет адреса"
        phone_number = self.user.phone_number if self.user.phone_number else "Нет телефона"
        return f'Имя: {self.user.name}, Телефон: {phone_number}'


class Request(models.Model):
    name_owner = models.ForeignKey(FlatOwner, models.CASCADE, null=True, verbose_name="Владелец")
    tsj = models.ForeignKey(TSJ, models.CASCADE, null=True, verbose_name="ТСЖ")
    number_flat = models.ForeignKey(Flat, models.CASCADE, null=True, verbose_name="Номер квартиры")
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField()
    phone_number = PhoneNumberField(null=True, blank=True, help_text='Пример: +996700777777',
                                    verbose_name='Номер телефона')
    created_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата создания")
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Ожидает'),
        ('approved', 'Одобрен'),
        ('rejected', 'Отклонен')], default='pending', null=True, verbose_name="Статус")

    def clean(self):
        existing_user_email = User.objects.filter(email=self.email).first()
        existing_user_phone = User.objects.filter(phone_number=self.phone_number).first()

        if existing_user_email:
            raise ValidationError(f"Пользователь с электронной почтой {self.email} уже существует.")
        elif existing_user_phone:
            raise ValidationError(f"Пользователь с номером телефона {self.phone_number} уже существует.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызов валидации перед сохранением
        if self.status == 'approved':
            super().save(*args, **kwargs)
            user = User.objects.create_user(
                role='TENANT',
                email=self.email,
                name=self.name,
                phone_number=self.phone_number,
                is_approved=True
            )
            # SendSMS.send_password_sms(user)
            user.save()
        else:
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Запросы'
        verbose_name_plural = 'Запросы'

    def __str__(self):
        return self.name


class ResidenceCertificate(models.Model):
    owner_name = models.CharField(max_length=100, verbose_name="Фамилия владельца", null=True)
    tenant_name = models.CharField(max_length=100, blank=True, verbose_name="Фамилия жителя", null=True)
    address = models.CharField(max_length=100, verbose_name="Точный адрес", null=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Выдано",
                                limit_choices_to={"role": "MANAGER"}, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True, verbose_name="Дата выдачи", null=True)

    class Meta:
        verbose_name = "Справка о местожительстве"
        verbose_name_plural = "Справки о местожительстве"

    def __str__(self):
        return f"Справка для {self.owner_name}"


# class ResidentHistory(models.Model):
#     flat = models.ForeignKey(Flat, on_delete=models.CASCADE, verbose_name="Квартира")
#     resident_surname = models.CharField(max_length=100, verbose_name="Фамилия жителя")
#     start_date = models.DateField(verbose_name="Дата начала проживания")
#     end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания проживания")
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец на момент проживания")
#
#     class Meta:
#         verbose_name = "История жителей квартиры"
#         verbose_name_plural = "История жителей квартир"
#
#     def __str__(self):
#         return f"{self.resident_surname} в квартире {self.flat}"
