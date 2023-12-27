from rest_framework import serializers

from .models import *


class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'is_moderator')


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


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)