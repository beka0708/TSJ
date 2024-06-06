# Generated by Django 5.0.6 on 2024-06-06 10:41

import django.db.models.deletion
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Ссылка на камеру')),
            ],
            options={
                'verbose_name': 'Камера',
                'verbose_name_plural': 'Камеры',
            },
        ),
        migrations.CreateModel(
            name='DomKom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание')),
                ('url', models.URLField(blank=True, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Мой дом',
                'verbose_name_plural': 'Мой дом',
            },
        ),
        migrations.CreateModel(
            name='HelpInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('url', models.URLField(verbose_name='Ссылка')),
                ('number', models.CharField(max_length=32, verbose_name='Служебный номер')),
            ],
            options={
                'verbose_name': 'Полезная Информация',
                'verbose_name_plural': 'Полезная Информация',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/', verbose_name='Фотография')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Добавить фото',
            },
        ),
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_date', models.DateField()),
                ('flat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.flat')),
            ],
            options={
                'verbose_name': 'Задолженности квартиры',
                'verbose_name_plural': 'Задолженности квартиры',
            },
        ),
    ]
