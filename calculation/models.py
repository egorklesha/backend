from datetime import datetime, date
# Модель юзера джанговская
from django.contrib.auth.models import User
from django.db import models

from django.utils import timezone


# Услуга
class Indicator(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", default="Описание")
    type = models.CharField(verbose_name="Единица измерения")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    image = models.ImageField(default="indicators/default.jpg", verbose_name="Фото")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Показатель"
        verbose_name_plural = "Показатели"


# Заявка
class Estimate(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершён'),
        (4, 'Отменён'),
        (5, 'Удалён'),
    )

    apartment = models.IntegerField(default=255, verbose_name="Номер квартиры")

    status = models.IntegerField(max_length=100, choices=STATUS_CHOICES, default=1, verbose_name="Статус")
    date_estimate = models.DateField(default=date.today(), verbose_name="Дата расчета")
    date_created = models.DateTimeField(default=datetime.now(tz=timezone.utc), verbose_name="Дата создания")
    date_of_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Модератор", related_name='moderator', null=True)

    def __str__(self):
        return "Рассчет №" + str(self.pk)

    class Meta:
        verbose_name = "Рассчет"
        verbose_name_plural = "Рассчеты"
        ordering = ('-date_of_formation', )


# м-м
class IndicatorEstimate(models.Model):
    indicator = models.ForeignKey(Indicator, models.CASCADE, blank=True, null=True)
    estimate = models.ForeignKey(Estimate, models.CASCADE, blank=True, null=True)
    value = models.FloatField(verbose_name="Значение счётчика", default=1000)

    def __str__(self):
        return "Показатель-Расчет №" + str(self.pk)

    class Meta:
        verbose_name = "Показатель-Расчет"
        verbose_name_plural = "Показатели-Расчеты"
