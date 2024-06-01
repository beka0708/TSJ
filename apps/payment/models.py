from django.db import models
from django.contrib.auth import get_user_model
from apps.home.models import Flat

User = get_user_model()

STATUS_CHOICES = (
    ('pending', 'Ожидание'),
    ('approved', 'Оплачено'),
    ('rejected', 'Отклонено'),
)


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


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, null=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.user.name} плата за {self.payment_type} {self.flat}"

    class Meta:
        verbose_name = "Принятие платежей"
        verbose_name_plural = "Принятие платежей"
