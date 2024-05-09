from django.contrib.auth import get_user_model
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from apps.home.models import TSJ
from apps.userprofile.models import Profile

User = get_user_model()


class DomKom(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = CKEditor5Field(verbose_name="Описание")
    url = models.URLField(blank=True, verbose_name="Ссылка")
    image = models.ImageField(upload_to='media/', verbose_name="Фото")
    info = models.OneToOneField(User, on_delete=models.CASCADE,
                                limit_choices_to={"role": "MANAGER"}, verbose_name="Информация о домкоме")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Мой дом"
        verbose_name_plural = "Мой дом"


class Camera(models.Model):
    url = models.URLField(verbose_name="Ссылка на камеру")

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"


class Receipts(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    cost = models.PositiveIntegerField(verbose_name="Сумма к оплате")
    status = models.CharField(max_length=50, choices=[
        ("pending", "Не оплачено"),
        ("approved", "Оплачено"),
    ],
                              default="pending", verbose_name="Статус")
    deadline = models.DateTimeField(verbose_name="Конечный срок")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Квитанция"
        verbose_name_plural = "Квитанции"


class HelpInfo(models.Model):
    tsj = models.ForeignKey(TSJ, models.CASCADE, null=True, verbose_name="ТСЖ")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    url = models.URLField(verbose_name="Ссылка")
    number = models.CharField(max_length=32, verbose_name="Служебный номер")

    class Meta:
        verbose_name = "Полезная Информация"
        verbose_name_plural = "Полезная Информация"

    def __str__(self):
        return self.title


