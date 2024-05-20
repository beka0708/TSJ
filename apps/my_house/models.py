from django.contrib.auth import get_user_model
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from apps.home.models import TSJ, Flat, FlatOwner, FlatTenant
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


class PaymentType(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_recurring = models.BooleanField(default=False)
    period = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Перечень платежей"
        verbose_name_plural = "Перечень платежей"


STATUS_CHOICES = (
    ('pending', 'Ожидание'),
    ('approved', 'Оплачено'),
    ('rejected', 'Отклонено'),
)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, null=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.name} плата за квартиру {self.flat}"

    class Meta:
        verbose_name = "Принятие платежей"
        verbose_name_plural = "Принятие платежей"


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


