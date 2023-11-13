# Generated by Django 4.2.4 on 2023-11-12 16:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculation', '0004_alter_estimate_date_complete_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estimate',
            name='date_complete',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 12, 16, 9, 23, 684426, tzinfo=datetime.timezone.utc), verbose_name='Дата завершения'),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 12, 16, 9, 23, 683988, tzinfo=datetime.timezone.utc), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='date_of_formation',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 12, 16, 9, 23, 684420, tzinfo=datetime.timezone.utc), verbose_name='Дата формирования'),
        ),
    ]
