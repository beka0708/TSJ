# Generated by Django 5.0.6 on 2024-06-04 16:18

import django.db.models.deletion
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(verbose_name='Номер квартиры')),
            ],
            options={
                'verbose_name': 'Квартиру',
                'verbose_name_plural': 'Квартиры',
            },
        ),
        migrations.CreateModel(
            name='FlatTenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Квартиранта',
                'verbose_name_plural': 'Квартиранты',
            },
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_block', models.CharField(max_length=100, null=True, unique=True, verbose_name='Номер дома')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
                ('geo_position', models.URLField(verbose_name='Геолокация')),
                ('floors', models.PositiveIntegerField(verbose_name='Количество этажей')),
                ('entrances', models.PositiveIntegerField(verbose_name='Количество подъездов')),
                ('flats_number', models.PositiveIntegerField(verbose_name='Количество квартир')),
            ],
            options={
                'verbose_name': 'дом',
                'verbose_name_plural': 'Дома',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Новости', 'Новости'), ('Объявления', 'Объявления')], max_length=100, verbose_name='Тип')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание')),
                ('link', models.URLField(verbose_name='Ссылка на источник')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'новость',
                'verbose_name_plural': 'Новости',
            },
        ),
        migrations.CreateModel(
            name='NewsView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Просмотр новости',
                'verbose_name_plural': 'Просмотры новостей',
            },
        ),
        migrations.CreateModel(
            name='Request_Vote_News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.CharField(choices=[('Новость', 'Новость'), ('Голосование', 'Голосование')], max_length=20, verbose_name='Новость или Голосование')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('link', models.URLField(blank=True, help_text='для новостей', verbose_name='Ссылка на источник')),
                ('deadline_date', models.DateTimeField(blank=True, help_text='для голосование', verbose_name='Срок голосования')),
                ('status', models.CharField(choices=[('pending', 'Ожидает'), ('approved', 'Опубликован'), ('rejected', 'Отклонен')], default='pending', max_length=50, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Запросы на голосование',
                'verbose_name_plural': 'Запросы на голосование',
            },
        ),
        migrations.CreateModel(
            name='TSJ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название ТСЖ')),
            ],
            options={
                'verbose_name': 'ТСЖ',
                'verbose_name_plural': 'ТСЖ',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('deadline', models.DateTimeField(verbose_name='Конец голосование')),
                ('yes_count', models.IntegerField(default=0, verbose_name='Количество ответов "за')),
                ('no_count', models.IntegerField(default=0, verbose_name='Количество ответов "нет')),
            ],
            options={
                'verbose_name': 'Голосование',
                'verbose_name_plural': 'Голосование',
            },
        ),
        migrations.CreateModel(
            name='VoteResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_value', models.CharField(max_length=10, verbose_name='Голос')),
            ],
            options={
                'verbose_name': 'Результат',
                'verbose_name_plural': 'Результаты',
            },
        ),
        migrations.CreateModel(
            name='VoteView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(auto_now_add=True, verbose_name='Время просмотра')),
            ],
            options={
                'verbose_name': 'Просмотр',
                'verbose_name_plural': 'Просмотры',
            },
        ),
        migrations.CreateModel(
            name='ApartmentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change_date', models.DateField(verbose_name='Дата создания')),
                ('description', models.TextField(verbose_name='Информация')),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.flat', verbose_name='Квартира')),
            ],
            options={
                'verbose_name': 'История квартир',
                'verbose_name_plural': 'История квартир',
            },
        ),
        migrations.CreateModel(
            name='FlatOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateField(auto_now_add=True, null=True)),
                ('flat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.flat', verbose_name='Квартира')),
            ],
            options={
                'verbose_name': 'владелец',
                'verbose_name_plural': 'Владельцы',
            },
        ),
    ]
