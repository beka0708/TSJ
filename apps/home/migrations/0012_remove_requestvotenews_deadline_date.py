# Generated by Django 5.0.6 on 2024-06-20 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_requestvotenews_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestvotenews',
            name='deadline_date',
        ),
    ]