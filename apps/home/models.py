from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()


class TSJ(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название ТСЖ")
    house = models.ManyToManyField('House', verbose_name="Дома для ТСЖ")

    class Meta:
        verbose_name = "ТСЖ"
        verbose_name_plural = "Добавить ТСЖ"

    def __str__(self):
        return self.name


class House(models.Model):
    name_block = models.CharField(max_length=100, null=True, verbose_name="Номер дома")
    address = models.CharField(max_length=200, verbose_name="Адрес")
    geo_position = models.URLField(verbose_name="Геолокация")
    floors = models.PositiveIntegerField(verbose_name="Количество этажей")  # этажи
    entrances = models.PositiveIntegerField(verbose_name="Количество подъездов")  # подъезды
    flats_number = models.PositiveIntegerField(verbose_name="Количество квартир")  # квартиры

    class Meta:
        verbose_name = "Дома"
        verbose_name_plural = "Добавить дом"

    def __str__(self):
        return self.name_block


class FlatOwner(models.Model):
    tsj = models.ForeignKey(TSJ, on_delete=models.CASCADE, null=True, verbose_name="ТСЖ")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    flat = models.ForeignKey('Flat', on_delete=models.CASCADE, verbose_name="Квартира")

    class Meta:
        verbose_name = "Владельцы"
        verbose_name_plural = "Добавить владельца"

    def __str__(self):
        return f'Владелец: {self.user.get_full_name()}, Квартира: {self.flat}'


class FlatTenant(models.Model):
    tsj = models.ForeignKey(TSJ, on_delete=models.CASCADE, null=True, verbose_name="ТСЖ")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Арендатор")
    flat = models.ForeignKey('Flat', on_delete=models.CASCADE, verbose_name="Квартира")
    owner = models.ForeignKey('FlatOwner', models.CASCADE, null=True, verbose_name="Владелец квартиры")

    class Meta:
        verbose_name = "Квартирант"
        verbose_name_plural = "Добавить квартиранта"

    def __str__(self):
        return f'Квартирант: {self.user.get_full_name()}, Квартира {self.flat}'


class Flat(models.Model):
    house = models.ForeignKey('House', models.CASCADE, null=True, verbose_name="Дом")
    number = models.PositiveIntegerField(verbose_name="Номер квартиры")

    class Meta:
        verbose_name = "Квартиры"
        verbose_name_plural = "Добавить квартиру"

    def __str__(self):
        return f'Дом - {self.house.name_block}, Квартира {self.number}' \
            if self.house else 'No house assigned'


TYPE = {
    'Новости': 'Новости',
    'Объявления': 'Объявления'
}


class News(models.Model):
    tsj = models.ForeignKey('TSJ', models.CASCADE, null=True, verbose_name="ТСЖ")
    type = models.CharField(max_length=100, choices=TYPE, verbose_name="Тип")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    link = models.URLField(verbose_name="Ссылка на источник")
    created_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата создания")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Новости"
        verbose_name_plural = "Добавить новость"

    def __str__(self):
        return self.title


TYPE_OWNERS = {
    'Житель': 'Житель',
    'Квартирант': 'Квартирант'
}


class Request(models.Model):
    name_owner = models.ForeignKey(FlatOwner, models.CASCADE, null=True, verbose_name="Владелец")
    tsj = models.ForeignKey(TSJ, models.CASCADE, null=True, verbose_name="ТСЖ")
    number_flat = models.ForeignKey(Flat, models.CASCADE, null=True, verbose_name="Номер квартиры")
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField()
    number_phone = PhoneNumberField('Номер телефона', help_text='Пример: +996700777777', null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата создания")
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Ожидает'),
        ('approved', 'Одобрен'),
        ('rejected', 'Отклонен')], default='pending', null=True, verbose_name="Статус")

    class Meta:
        verbose_name = 'Запросы'
        verbose_name_plural = 'Запросы'

    def __str__(self):
        return self.name


class HelpInfo(models.Model):
    tsj = models.ForeignKey(TSJ, models.CASCADE, null=True, verbose_name="ТСЖ")
    title = models.CharField(max_length=100, verbose_name="Заголовок", null=True, blank=True)
    url = models.URLField(verbose_name="Ссылка")
    number = models.CharField(max_length=32, verbose_name="Служебный номер")

    class Meta:
        verbose_name = 'Полезная Информация'
        verbose_name_plural = 'Полезная Информация'

    def __str__(self):
        return self.title


VOTING = {
    'Я за': 'Я за',
    'Я против': 'Я против',
    'Вариантный': 'Вариантный'
}


class Vote(models.Model):
    tsj = models.ForeignKey(TSJ, on_delete=models.CASCADE, verbose_name="ТСЖ")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    vote_type = models.CharField(max_length=50, choices=VOTING, null=True, verbose_name="Выбор")
    users_votes = models.ManyToManyField(User, verbose_name="Проголосовавшие")
    created_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Дата создания")
    end_date = models.DateTimeField(null=True, verbose_name="Дата окончания")

    class Meta:
        verbose_name = 'Голосование'
        verbose_name_plural = 'Голосование'

    def __str__(self):
        return self.title


class VoteNew(models.Model):
    tjs = models.ForeignKey(TSJ, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    yes_count = models.IntegerField(default=0)
    no_count = models.IntegerField(default=0)


    def __str__(self):
        return self.title


class Votes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.CharField(max_length=10)
    vote_new = models.ForeignKey(VoteNew, related_name='votes', on_delete=models.CASCADE)


# class VoteRecord(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     vote = models.ForeignKey(VoteNew, on_delete=models.CASCADE)
#     choice = models.CharField(max_length=3, choices=(("да", "Да"), ("нет", "Нет")))

# class BaseVoting(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     vote_type = models.CharField(max_length=50, choices=[('за/против', 'за/против'), ('вариативный', 'вариативный')])
#     tsj = models.ForeignKey(TSJ, on_delete=models.CASCADE)
#     users_votes = models.ManyToManyField(User)
# #
#     class Meta:
#         abstract = True
#
# class AdminVoting(BaseVoting):
#     vote_type = models.CharField(max_length=50, choices=[('за/против', 'за/против'), ('вариативный', 'вариативный')],
#     blank=True, null=True)
#
# class UserVoting(BaseVoting):
#     vote_type = models.CharField(max_length=50, choices=[('за/против', 'за/против'), ('вариативный', 'вариативный')],
#     blank=False, null=False)
