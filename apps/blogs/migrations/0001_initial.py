# Generated by Django 5.0.6 on 2024-06-04 17:47

import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                'verbose_name': 'Новости',
                'verbose_name_plural': 'Новость',
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
    ]
