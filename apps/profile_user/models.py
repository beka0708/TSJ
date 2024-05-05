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
        return f'{self.user.name} '

    def update_profile(self, name=None, email=None, phone_number=None, address=None):
        user = self.user
        if name:
            user.name = name
        if email:
            user.email = email
        if phone_number:
            user.phone_number = phone_number
        if address:
            user.address = address
        user.save()


