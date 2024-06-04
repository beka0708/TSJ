from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth import get_user_model
from apps.home.models import TSJ
User = get_user_model()

TYPE = {"Новости": "Новости", "Объявления": "Объявления"}


class News(models.Model):
    tsj = models.ForeignKey(TSJ, models.CASCADE, null=True, verbose_name="ТСЖ")
    type = models.CharField(max_length=100, choices=TYPE, verbose_name="Тип")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = CKEditor5Field(verbose_name="Описание")
    link = models.URLField(verbose_name="Ссылка на источник")
    created_date = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="Дата создания"
    )
    update_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Новости"
        verbose_name_plural = "Новость"

    def __str__(self):
        return self.title


class NewsView(models.Model):
    news = models.ForeignKey(News, related_name='views', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Просмотр новости"
        verbose_name_plural = "Просмотры новостей"

    def __str__(self):
        return self.user.name
