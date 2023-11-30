from rest_framework import serializers

from .models import *


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = "__all__"


class EstimateSerializer(serializers.ModelSerializer):
    services = IndicatorSerializer(read_only=True, many=True)

    class Meta:
        model = Estimate
        fields = "__all__"

