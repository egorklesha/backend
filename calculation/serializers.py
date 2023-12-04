from rest_framework import serializers

from .models import *


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')


class EstimateSerializer(serializers.ModelSerializer):
    indicators = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    def get_indicators(self, estimate):
        items = IndicatorEstimate.objects.filter(estimate=estimate)
        return IndicatorSerializer([item.indicator for item in items], many=True).data

    class Meta:
        model = Estimate
        fields = "__all__"


class IndicatorEstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndicatorEstimate
        fields = "__all__"