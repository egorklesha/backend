from django.contrib import admin
from .models import *

admin.site.register(Indicator)
admin.site.register(Estimate)
admin.site.register(CustomUser)
admin.site.register(IndicatorEstimate)