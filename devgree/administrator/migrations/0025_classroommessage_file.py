# Generated by Django 3.2.9 on 2022-02-24 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0024_auto_20220220_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroommessage',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='classroom_files'),
        ),
    ]