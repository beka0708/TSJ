from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Владелец")
    cover = models.ImageField(upload_to='covers/', null=True, blank=True, verbose_name="Обложка")

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        email = self.user.email if self.user.email else "Нет email"
        address = self.user.address if self.user.address else "Нет адреса"
        phone_number = self.user.phone_number if self.user.phone_number else "Нет телефона"
        return f'Имя: {self.user.name}, Email: {email}, Адрес: {address}, Телефон: {phone_number}'
