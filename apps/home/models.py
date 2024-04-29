from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TSJ(models.Model):
    name = models.CharField(max_length=100)
    house = models.ManyToManyField('House')

    class Meta:
        verbose_name = "ТСЖ"
        verbose_name_plural = "Добавить ТСЖ"

    def __str__(self):
        return self.name


class House(models.Model):
    name_block = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200)
    geo_position = models.URLField()
    floors = models.PositiveIntegerField()  # этажи
    entrances = models.PositiveIntegerField()  # подъезды
    flats_number = models.PositiveIntegerField()  # квартиры

    class Meta:
        verbose_name = "Дома"
        verbose_name_plural = "Добавить дом"

    def __str__(self):
        return self.name_block


class FlatOwner(models.Model):
    tsj = models.ForeignKey(TSJ, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flat = models.ForeignKey('Flat', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Владельцы"
        verbose_name_plural = "Добавить владельца"

    def __str__(self):
        return f'Владелец: {self.user.get_full_name()}, Квартира: {self.flat}'


class FlatTenant(models.Model):
    tsj = models.ForeignKey(TSJ, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flat = models.ForeignKey('Flat', on_delete=models.CASCADE)
    owner = models.ForeignKey('FlatOwner', models.CASCADE, null=True)

    class Meta:
        verbose_name = "Квартирант"
        verbose_name_plural = "Добавить квартиранта"

    def __str__(self):
        return f'Квартирант: {self.user.get_full_name()}, Квартира {self.flat}'


class Flat(models.Model):
    house = models.ForeignKey('House', models.CASCADE, null=True)
    number = models.PositiveIntegerField()

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
    tsj = models.ForeignKey('TSJ', models.CASCADE, null=True)
    type = models.CharField(max_length=100, choices=TYPE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True)

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
    name_owner = models.ForeignKey(FlatOwner, models.CASCADE, null=True)
    tsj = models.ForeignKey(TSJ, models.CASCADE, null=True)
    number_flat = models.ForeignKey(Flat, models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number_phone = models.CharField(max_length=32, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Ожидает'),
        ('approved', 'Одобрен'),
        ('rejected', 'Отклонен')], default='pending', null=True)

    class Meta:
        verbose_name = 'Запросы'
        verbose_name_plural = 'Запросы'

    def __str__(self):
        return self.name


class HelpInfo(models.Model):
    tsj = models.ForeignKey(TSJ, models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    url = models.URLField()
    number = models.CharField(max_length=32)

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
    tsj = models.ForeignKey(TSJ, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    vote_type = models.CharField(max_length=50, choices=VOTING, null=True)
    users_votes = models.ManyToManyField(User)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    end_date = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'Голосование'
        verbose_name_plural = 'Голосование'

    def __str__(self):
        return self.title

# class BaseVoting(models.Model):
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     vote_type = models.CharField(max_length=50, choices=[('за/против', 'за/против'), ('вариативный', 'вариативный')])
#     tsj = models.ForeignKey(TSJ, on_delete=models.CASCADE)
#     users_votes = models.ManyToManyField(User)
#
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
