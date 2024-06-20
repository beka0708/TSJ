# Generated by Django 5.0.6 on 2024-06-20 04:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_deadline_alter_vote_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestvotenews',
            name='deadline',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.deadline', verbose_name='Срок голосования'),
        ),
    ]
