# Generated by Django 5.0.6 on 2024-06-19 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_room_participants_room_tsj_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='tsj_id',
            new_name='tsj',
        ),
    ]
