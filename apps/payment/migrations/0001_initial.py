# Generated by Django 5.0.6 on 2024-06-04 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_recurring', models.BooleanField(default=False)),
                ('period', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Перечень платежей',
                'verbose_name_plural': 'Перечень платежей',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('pending', 'Ожидание'), ('approved', 'Оплачено'), ('rejected', 'Отклонено')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('flat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.flat')),
            ],
            options={
                'verbose_name': 'Принятие платежей',
                'verbose_name_plural': 'Принятие платежей',
            },
        ),
    ]
