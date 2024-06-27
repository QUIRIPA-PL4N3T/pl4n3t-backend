from rest_framework import serializers
from .models import Activity, ActivityGasEmitted, ActivityGasEmittedByFactor


class ActivityGasEmittedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityGasEmitted
        fields = '__all__'


class ActivityGasEmittedByFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityGasEmittedByFactor
        fields = '__all__'


class ActivityListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['total_co2e']


class ActivitySerializer(serializers.ModelSerializer):
    gases_emitted = ActivityGasEmittedSerializer(many=True, read_only=True)
    gases_emitted_by_factor = ActivityGasEmittedByFactorSerializer(many=True, read_only=True)
    user_created = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['total_co2e']

    def create(self, validated_data):
        activity = super().create(validated_data)
        activity.save_gases_emitted()
        return activity

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.save_gases_emitted()
        return instance
