import random

from django.core import management
from django.core.management.base import BaseCommand
from .utils import random_date, random_timedelta
from ...models import *


def add_indicators():
    Indicator.objects.create(
        name="Электроэнергия",
        description="Электроэнергия это — физический термин, широко распространённый в технике и в быту для определения количества электрической энергии, выдаваемой генератором в электрическую сеть или получаемой из сети потребителем.",
        type="кВт.ч",
        image="indicators/1.jpg"
    )

    Indicator.objects.create(
        name="Отопление",
        description="Отопление это — искусственный обогрев помещений с целью возмещения в них теплопотерь и поддержания на заданном уровне температуры, отвечающей условиям теплового комфорта и/или требованиям технологического процесса.",
        type="ГКал",
        image="indicators/2.jpg"
    )

    Indicator.objects.create(
        name="Холодное водоснабжение",
        description="Холодное водоснабжение это — круглосуточное обеспечение потребителя холодной питьевой водой надлежащего качества, подаваемой в необходимых объемах по присоединенной сети в жилое помещение либо до водоразборной колонки.",
        type="м3",
        image="indicators/3.jpg"
    )

    Indicator.objects.create(
        name="Горячее водоснабжение",
        description="Холодное водоснабжение это — круглосуточное обеспечение потребителя холодной питьевой водой надлежащего качества, подаваемой в необходимых объемах по присоединенной сети в жилое помещение либо до водоразборной колонки.",
        type="м3",
        image="indicators/4.jpg"
    )

    print("Услуги добавлены")


def add_estimates():
    owners = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(owners) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    indicators = Indicator.objects.all()

    for _ in range(30):
        estimate = Estimate.objects.create()
        estimate.name = "Косметика №" + str(estimate.pk)
        estimate.status = random.randint(2, 5)

        if estimate.status in [3, 4]:
            estimate.closed_date = random_date()
            estimate.formated_date = estimate.closed_date - random_timedelta()
            estimate.created_date = estimate.formated_date - random_timedelta()
        else:
            estimate.formated_date = random_date()
            estimate.created_date = estimate.formated_date - random_timedelta()

        estimate.owner = random.choice(owners)
        estimate.moderator = random.choice(moderators)

        for i in range(random.randint(1, 3)):
            try:
                item = IndicatorEstimate.objects.create()
                item.estimate = estimate
                item.indicator = random.choice(indicators)
                item.save()
            except Exception as e:
                print(e)

        estimate.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_indicators()
        add_estimates()









