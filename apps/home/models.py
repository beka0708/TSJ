from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


User = get_user_model()


class TSJ(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название ТСЖ")
    house = models.ManyToManyField("House", verbose_name="Дома для ТСЖ")

    class Meta:
        verbose_name = "ТСЖ"
        verbose_name_plural = "ТСЖ"

    def __str__(self):
        return self.name


class House(models.Model):
    """Дом"""
    name_block = models.CharField(
        max_length=100, null=True, verbose_name="Номер дома", unique=True
    )
    address = models.CharField(max_length=200, verbose_name="Адрес")
    geo_position = models.URLField(verbose_name="Геолокация")
    floors = models.PositiveIntegerField(verbose_name="Количество этажей")  # этажи
    entrances = models.PositiveIntegerField(
        verbose_name="Количество подъездов"
    )  # подъезды
    flats_number = models.PositiveIntegerField(
        verbose_name="Количество квартир"
    )  # квартиры

    developer = models.ForeignKey('HouseDeveloper', on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        super().clean()
        if House.objects.filter(name_block=self.name_block).exists():
            raise ValidationError("Дом с таким номером уже существует.")

    class Meta:
        verbose_name = "дом"
        verbose_name_plural = "Дома"

    def __str__(self):
        return self.name_block


class HousePhoto(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='albums/')


class DomKomRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    houses = models.ManyToManyField(House)

    def __str__(self):
        return self.user.name


class FlatOwner(models.Model):
    """Владелец квартиры"""
    tsj = models.ForeignKey(
        TSJ, on_delete=models.CASCADE, null=True, verbose_name="ТСЖ"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        limit_choices_to={"role": "OWNER"}, null=True
    )
    flat = models.ForeignKey("Flat", on_delete=models.CASCADE, verbose_name="Квартира")
    created_date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "владелец"
        verbose_name_plural = "Владельцы"

    def __str__(self):
        return f"Владелец: {self.user.name}, Квартира: {self.flat}"


class FlatTenant(models.Model):
    tsj = models.ForeignKey(
        TSJ, on_delete=models.CASCADE, null=True, verbose_name="ТСЖ"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Арендатор",
        limit_choices_to={"role": "TENANT"},
    )
    flat = models.ForeignKey("Flat", on_delete=models.CASCADE, verbose_name="Квартира")
    owner = models.ForeignKey(
        "FlatOwner", on_delete=models.CASCADE, null=True, verbose_name="Владелец квартиры"
    )
    created_date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Квартиранта"
        verbose_name_plural = "Квартиранты"

    def __str__(self):
        return f"Квартирант: {self.user.name}, Квартира {self.flat}"


class Flat(models.Model):
    """
    Квартира
    """
    house = models.ForeignKey("House", models.CASCADE, null=True, verbose_name="Дом")
    number = models.PositiveIntegerField(verbose_name="Номер квартиры")

    class Meta:
        verbose_name = "Квартиру"
        verbose_name_plural = "Квартиры"
        unique_together = (("house", "number"),)

    def __str__(self):
        return (
            f"Дом - {self.house.name_block}, Квартира {self.number}"
            if self.house
            else "No house assigned"
        )

    def get_owner(self):
        return ", ".join(owner.user.name for owner in self.flatowner_set.all())


class ApartmentHistory(models.Model):
    """
    История квартиры
    """
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, verbose_name="Квартира")
    owner = models.ForeignKey(FlatOwner, on_delete=models.CASCADE, related_name='user_history',
                              null=True, verbose_name="Владелец")
    tenant = models.ManyToManyField(FlatTenant, related_name='resident_history',
                                    blank=True, verbose_name="Арендатор")
    change_date = models.DateField(verbose_name="Дата создания")
    description = models.TextField(verbose_name="Информация")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "История квартир"
        verbose_name_plural = "История квартир"


class Vote(models.Model):
    """Голосование"""
    tjs = models.ForeignKey(TSJ, on_delete=models.CASCADE, verbose_name="Выберите ТСЖ")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = CKEditor5Field(verbose_name="Описание")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    deadline = models.DateTimeField(verbose_name="Конец голосование")
    yes_count = models.IntegerField(default=0, verbose_name='Количество ответов "за')
    no_count = models.IntegerField(default=0, verbose_name='Количество ответов "нет')
    room = models.OneToOneField("chat.Room", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Канал обсуждения")

    class Meta:
        verbose_name = "Голосование"
        verbose_name_plural = "Голосование"

    def __str__(self):
        return self.title


class VoteResult(models.Model):
    """Результаты голосвании"""
    vote = models.ForeignKey(Vote, related_name='votes', on_delete=models.CASCADE, verbose_name="Голосование")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    vote_value = models.CharField(max_length=10, verbose_name="Голос")  # 'за' или 'против'

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"

    def __str__(self):
        return self.user.name


class VoteView(models.Model):
    """Просмотр голосовании"""
    vote = models.ForeignKey(Vote, related_name='views', on_delete=models.CASCADE, verbose_name="Голосование")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name="Время просмотра")

    class Meta:
        verbose_name = "Просмотр"
        verbose_name_plural = "Просмотры"

    def __str__(self):
        return self.user.name


VOTING = {
    "Новость": "Новость",
    "Голосование": "Голосование",
}


class RequestVoteNews(models.Model):
    """
    Запросы на добавление голосования
    """
    tsj = models.ForeignKey(TSJ, on_delete=models.CASCADE, verbose_name="ТСЖ")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name="От пользователя")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = CKEditor5Field(verbose_name="Описание")
    created_date = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="Дата создания"
    )
    deadline_date = models.DateTimeField(
        blank=True, verbose_name="Срок голосования", help_text="для голосование"
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Ожидает"),
            ("approved", "Опубликован"),
            ("rejected", "Отклонен"),
        ],
        default="pending",
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Запросы на голосование"
        verbose_name_plural = "Запросы на голосование"

    def __str__(self):
        return self.title


class HouseDeveloper(models.Model):
    name = models.CharField(max_length=255)
    web_site = models.URLField()

    def __str__(self):
        return self.name
