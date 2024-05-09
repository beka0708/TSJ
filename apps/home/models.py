from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()


class TSJ(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название ТСЖ")
    house = models.ManyToManyField("House", verbose_name="Дома для ТСЖ")

    class Meta:
        verbose_name = "ТСЖ"
        verbose_name_plural = "Добавить ТСЖ"

    def __str__(self):
        return self.name


class House(models.Model):
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

    def clean(self):
        super().clean()
        if House.objects.filter(name_block=self.name_block).exists():
            raise ValidationError("Дом с таким номером уже существует.")

    class Meta:
        verbose_name = "Дома"
        verbose_name_plural = "Добавить дом"

    def __str__(self):
        return self.name_block


class FlatOwner(models.Model):
    tsj = models.ForeignKey(
        TSJ, on_delete=models.CASCADE, null=True, verbose_name="ТСЖ"
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        limit_choices_to={"role": "OWNER"},
    )
    flat = models.ForeignKey("Flat", on_delete=models.CASCADE, verbose_name="Квартира")

    class Meta:
        verbose_name = "Владельцы"
        verbose_name_plural = "Добавить владельца"

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
        "FlatOwner", models.CASCADE, null=True, verbose_name="Владелец квартиры"
    )

    class Meta:
        verbose_name = "Квартирант"
        verbose_name_plural = "Добавить квартиранта"

    def __str__(self):
        return f"Квартирант: {self.user.name}, Квартира {self.flat}"


class Flat(models.Model):
    house = models.ForeignKey("House", models.CASCADE, null=True, verbose_name="Дом")
    number = models.PositiveIntegerField(verbose_name="Номер квартиры")

    class Meta:
        verbose_name = "Квартиры"
        verbose_name_plural = "Добавить квартиру"
        unique_together = (("house", "number"),)

    def __str__(self):
        return (
            f"Дом - {self.house.name_block}, Квартира {self.number}"
            if self.house
            else "No house assigned"
        )


TYPE = {"Новости": "Новости", "Объявления": "Объявления"}


class News(models.Model):
    tsj = models.ForeignKey("TSJ", models.CASCADE, null=True, verbose_name="ТСЖ")
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
        verbose_name_plural = "Добавить новость"

    def __str__(self):
        return self.title


TYPE_OWNERS = {
    "Житель": "Житель",
    "Квартирант": "Квартирант"
}


class Vote(models.Model):
    tjs = models.ForeignKey(TSJ, on_delete=models.CASCADE, verbose_name="Выберите ТСЖ")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = CKEditor5Field(verbose_name="Описание")
    created_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(verbose_name="Конец голосование")
    yes_count = models.IntegerField(default=0, verbose_name='количество ответов "за')
    no_count = models.IntegerField(default=0, verbose_name='количество ответов "нет')

    class Meta:
        verbose_name = "Голосование"
        verbose_name_plural = "Голосование"

    def __str__(self):
        return self.title


class Votes(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"role": "OWNER"}
    )
    vote = models.CharField(max_length=10)
    vote_new = models.ForeignKey(Vote, related_name="votes", on_delete=models.CASCADE)


VOTING = {
    "Новость": "Новость",
    "Голосование": "Голосование",
}


class Request_Vote_News(models.Model):
    tsj = models.ForeignKey(TSJ, on_delete=models.CASCADE, verbose_name="ТСЖ")
    choice = models.CharField(
        max_length=20, choices=VOTING, verbose_name="Новость или Голосование"
    )
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = CKEditor5Field(verbose_name="Описание")
    created_date = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="Дата создания"
    )
    link = models.URLField(
        blank=True, verbose_name="Ссылка на источник", help_text="для новостей"
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
