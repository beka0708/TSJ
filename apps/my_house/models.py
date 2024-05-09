from django.contrib.auth import get_user_model
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from apps.home.models import TSJ
from apps.userprofile.models import Profile

User = get_user_model()


class DomKom(models.Model):
    title = models.CharField(max_length=100)
    description = CKEditor5Field()
    url = models.URLField(blank=True)
    image = models.ImageField(upload_to='')
    info = models.OneToOneField(User, on_delete=models.CASCADE,
                                limit_choices_to={"role": "MANAGER"})

    def __str__(self):
        return self.title


class YourForms(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)


class Camera(models.Model):
    url = models.URLField()

    def __str__(self):
        return self.url


class Receipts(models.Model):
    title = models.CharField(max_length=100)
    cost = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=[
        ("pending", "Не оплачено"),
        ("approved", "Оплачено"),
    ],
                              default="pending", verbose_name="Статус")
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title


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


