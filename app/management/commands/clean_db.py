from django.core.management.base import BaseCommand
from ...models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Estimate.objects.all().delete()
        Indicator.objects.all().delete()
        CustomUser.objects.all().delete()