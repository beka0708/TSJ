from django.contrib.auth import get_user_model
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from apps.home.models import TSJ, Flat, FlatOwner, FlatTenant
from apps.payment.models import Payment

User = get_user_model()


class DomKom(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = CKEditor5Field(verbose_name="Описание")
    url = models.URLField(blank=True, verbose_name="Ссылка")
    info = models.OneToOneField(User, on_delete=models.CASCADE,
                                limit_choices_to={"role": "MANAGER"}, verbose_name="Информация о домкоме")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Домком"
        verbose_name_plural = "Домком"


class Photo(models.Model):
    dom_kom = models.ForeignKey(DomKom, related_name='photos', on_delete=models.CASCADE, verbose_name="Дом")
    image = models.ImageField(upload_to='media/', verbose_name="Фотография")

    def __str__(self):
        return f"{self.dom_kom.title} - {self.image.name}"

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Добавить фото"


class Debt(models.Model):
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, null=True)
    payment_type = models.ForeignKey(Payment, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateField()

    def __str__(self):
        return self.flat

    class Meta:
        verbose_name = "Задолженности квартиры"
        verbose_name_plural = "Задолженности квартиры"


class Camera(models.Model):
    url = models.URLField(verbose_name="Ссылка на камеру")

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"


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
