from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Добавить пользователя"

    def __str__(self):
        return self.name


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
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    flat = models.ForeignKey('Flat', on_delete=models.CASCADE)
    flat_tenant = models.ManyToManyField('FlatTenant', blank=True, null=True)

    class Meta:
        verbose_name = "Владельцы"
        verbose_name_plural = "Добавить владельца"

    def __str__(self):
        return f'Владелец: {self.user.name}, Квартира: {self.flat}'


class FlatTenant(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    flat = models.ForeignKey('Flat', on_delete=models.CASCADE)
    owner = models.ForeignKey('FlatOwner', models.CASCADE, null=True)

    class Meta:
        verbose_name = "Квартирант"
        verbose_name_plural = "Добавить квартиранта"

    def __str__(self):
        return f'Квартирант: {self.user.name}, Квартира {self.flat}'


class Flat(models.Model):
    houses = models.ForeignKey('House', models.CASCADE, null=True)
    number = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Квартиры"
        verbose_name_plural = "Добавить квартиру"

    def __str__(self):
        return f'Дом - {self.houses.name_block}, Квартира {self.number}' \
            if self.houses else 'No house assigned'


TYPE = {
    'Новости': 'Новости',
    'Объявления': 'Объявления'
}


class News(models.Model):
    tsj = models.ForeignKey('TSJ', models.CASCADE)
    type = models.CharField(max_length=100, choices=TYPE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()

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
    name = models.CharField(max_length=100)
    email = models.EmailField()
    number_phone = models.PositiveIntegerField()
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
    name = models.CharField(max_length=100)
    url = models.URLField()
    number = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Полезная Информация'
        verbose_name_plural = 'Полезная Информация'

    def __str__(self):
        return self.name


class Voting(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='', blank=True)

    class Meta:
        verbose_name = 'Голосование'
        verbose_name_plural = 'Голосование'

    def __str__(self):
        return self.title
