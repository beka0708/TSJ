# Generated by Django 5.0.4 on 2024-05-15 07:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("home", "0002_initial"),
        ("my_house", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="domkom",
            name="info",
            field=models.OneToOneField(
                limit_choices_to={"role": "MANAGER"},
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Информация о домкоме",
            ),
        ),
        migrations.AddField(
            model_name="helpinfo",
            name="tsj",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="home.tsj",
                verbose_name="ТСЖ",
            ),
        ),
        migrations.AddField(
            model_name="userpayment",
            name="flat",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="home.flat"
            ),
        ),
        migrations.AddField(
            model_name="userpayment",
            name="payment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="my_house.payment"
            ),
        ),
        migrations.AddField(
            model_name="userpayment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="debt",
            name="payment_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="my_house.userpayment"
            ),
        ),
    ]
