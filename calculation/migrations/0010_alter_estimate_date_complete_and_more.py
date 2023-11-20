# Generated by Django 4.2.7 on 2023-11-19 22:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0009_alter_estimate_date_complete_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='date_complete',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 19, 22, 51, 22, 414607, tzinfo=datetime.timezone.utc), verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 19, 22, 51, 22, 414398, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='date_of_formation',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 19, 22, 51, 22, 414600, tzinfo=datetime.timezone.utc), verbose_name='Дата формирования'),
        ),
    ]
