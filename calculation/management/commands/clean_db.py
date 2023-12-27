from django.core.management.base import BaseCommand
from calculation.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        IndicatorEstimate.objects.all().delete()
        Estimate.objects.all().delete()
        Indicator.objects.all().delete()
        CustomUser.objects.all().delete()