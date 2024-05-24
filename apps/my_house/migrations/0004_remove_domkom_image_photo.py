# Generated by Django 5.0.6 on 2024-05-24 05:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_house', '0003_paymenttype_alter_debt_payment_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domkom',
            name='image',
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/', verbose_name='Фотография')),
                ('dom_kom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='my_house.domkom', verbose_name='Дом')),
            ],
            options={
                'verbose_name': 'Мой дом фотография',
                'verbose_name_plural': 'Мой дом фотографии',
            },
        ),
    ]
