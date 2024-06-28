from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from documents.models import Document
from documents.serializer import BaseDocumentSerializer
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
    documents = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    gases_emitted = ActivityGasEmittedSerializer(many=True, read_only=True)
    gases_emitted_by_factor = ActivityGasEmittedByFactorSerializer(many=True, read_only=True)
    user_created = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Activity
        fields = '__all__'
        read_only_fields = ['id', 'total_co2e']

    def create(self, validated_data):
        documents_data = validated_data.pop('documents', [])
        user = self.context['request'].user
        activity = Activity.objects.create(**validated_data)
        activity.save_gases_emitted()
        self.save_documents(activity, documents_data, user)
        return activity

    def update(self, instance, validated_data):
        documents_data = validated_data.pop('documents', [])
        user = self.context['request'].user
        instance = super().update(instance, validated_data)
        instance.save_gases_emitted()
        self.save_documents(instance, documents_data, user)
        return instance

    def save_documents(self, activity, documents_data, user): # noqa
        for document_data in documents_data:
            Document.objects.create(
                file=document_data,
                content_type=ContentType.objects.get_for_model(activity),
                object_pk=activity.pk,
                user_created=activity.user_created
            )


class ActivityResponseSerializer(BaseDocumentSerializer):
    gases_emitted = ActivityGasEmittedSerializer(many=True, read_only=True)
    gases_emitted_by_factor = ActivityGasEmittedByFactorSerializer(many=True, read_only=True)
    user_created = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Activity
        fields = (
            'id',
            'emission_source',
            'location',
            'user_created',
            'name',
            'description',
            'consumption',
            'date',
            'month',
            'year',
            'unit',
            'total_co2e',
            'documents',
            'gases_emitted',
            'gases_emitted_by_factor',
        )
        read_only_fields = ['id', 'total_co2e']
