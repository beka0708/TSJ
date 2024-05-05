from django.contrib.auth import get_user_model
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
        return f'Имя: {self.user.name}, Email: {email}, Адрес: {address}, Телефон: {phone_number}'


class Request(models.Model):
    name_owner = models.ForeignKey(FlatOwner, models.CASCADE, null=True, verbose_name="Владелец")
    tsj = models.ForeignKey(TSJ, models.CASCADE, null=True, verbose_name="ТСЖ")
    number_flat = models.ForeignKey(Flat, models.CASCADE, null=True, verbose_name="Номер квартиры")
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField()
    number_phone = PhoneNumberField(null=True, blank=True, help_text='Пример: +996700777777',
                                    verbose_name='Номер телефона')
    created_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата создания")
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Ожидает'),
        ('approved', 'Одобрен'),
        ('rejected', 'Отклонен')], default='pending', null=True, verbose_name="Статус")

    class Meta:
        verbose_name = 'Запросы'
        verbose_name_plural = 'Запросы'

    def __str__(self):
        return self.name
