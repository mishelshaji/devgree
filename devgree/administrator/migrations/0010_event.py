# Generated by Django 3.2.9 on 2021-12-07 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0009_auto_20211206_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.department')),
            ],
        ),
    ]
