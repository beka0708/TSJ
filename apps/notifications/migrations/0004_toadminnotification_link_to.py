# Generated by Django 5.0.6 on 2024-06-12 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_toadminnotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='toadminnotification',
            name='link_to',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]