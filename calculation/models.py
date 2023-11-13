from datetime import datetime
from django.db import models, connection

from django.urls import reverse
from django.utils import timezone


class Indicator(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, default="Электроэнергия", verbose_name="Название")
    description = models.TextField(max_length=500, verbose_name="Описание", default="Описание")
    type = models.CharField(default="кВт.ч", verbose_name="Единица измерения")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(upload_to="indicators", default="indicators/default.jpg", verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Показатель"
        verbose_name_plural = "Показатели"

    def get_absolute_url(self):
        return reverse("indicator_details", kwargs={"indicator_id": self.id})

    def get_delete_url(self):
        return reverse("indicator_delete", kwargs={"indicator_id": self.id})

    def delete(self):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE calculation_indicator SET status = 2 WHERE id = %s", [self.pk])


class Estimate(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    value = models.IntegerField(default=10, verbose_name="Количество")
    apartment = models.IntegerField(default=255, verbose_name="Номер квартиры")

    status = models.IntegerField(max_length=100, choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_created = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата создания")
    date_of_formation = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата формирования")
    date_complete = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата завершения")

    def __str__(self):
        return "Рассчет №" + str(self.pk)

    class Meta:
        verbose_name = "Рассчет"
        verbose_name_plural = "Рассчеты"