# Generated by Django 3.2.9 on 2021-12-08 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0012_booking'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='event_id',
            new_name='event_name',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='room_id',
            new_name='room_name',
        ),
    ]
