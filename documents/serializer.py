from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import InMemoryUploadedFile
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from documents.models import Document
from documents.utils import is_multimedia_file, get_file_type


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(allow_empty_file=False, use_url=False)
    file_url = serializers.SerializerMethodField()
    thumbnails_url = serializers.SerializerMethodField(read_only=True)
    file_type = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(OpenApiTypes.URI)
    def get_file_url(self, document):
        try:
            request = self.context.get('request')
            file_url = document.file.url
            return request.build_absolute_uri(file_url)
        except AttributeError:
            return document.get_absolute_url()

    @extend_schema_field(OpenApiTypes.URI)
    def get_thumbnails_url(self, document: Document):
        if document.thumbnails:
            try:
                request = self.context.get('request')
                thumbnails_url = document.thumbnails.url
                return request.build_absolute_uri(thumbnails_url)
            except AttributeError:
                return document.get_thumbnails_absolute_url()
        return ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_file_type(self, obj: Document):
        return obj.document_content_type

    def validate(self, data):
        if not self.instance:
            file: InMemoryUploadedFile = data.get('file', None)
            if not file:
                raise ValidationError({'file': _('el archivo no puede ser nulo')})
            else:
                data['size'] = file.size
                data['file_type'] = file.content_type
                data['is_multimedia'] = is_multimedia_file(file.content_type)
        return data

    def create(self, validated_data):
        file: InMemoryUploadedFile = validated_data['file']
        validated_data['size'] = file.size
        validated_data['file_type'] = file.content_type

        try:
            instance = Document.objects.create(**validated_data)
        except TypeError:
            msg = 'Got a `TypeError`when calling Document.objects.create()'
            raise TypeError(msg)
        return instance

    class Meta:
        model = Document
        fields = ('id', 'file', 'file_type', 'title', 'user_created', 'updated', 'created',
                  'tags', 'is_multimedia', 'file_url', 'thumbnails_url', 'size', 'file_type')
        read_only_fields = ['id', 'updated', 'created', 'file_url', 'thumbnails_url',
                            'user_created', 'is_evidence', 'size', 'file_type']
        # extra_kwargs = {'file': {'write_only': True}}


class BaseDocumentSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(DocumentSerializer(many=True, read_only=True, allow_null=True))
    def get_documents(self, obj):
        documents = Document.objects.for_model(obj)
        request = self.context.get('request')
        serializer = DocumentSerializer(
            documents,
            many=True,
            allow_null=True,
            context={"request": request}
        )
        return serializer.data


class AvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True, allow_null=True)

    @extend_schema_field(DocumentSerializer(many=False, read_only=True, allow_null=True))
    def get_avatar(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        try:
            avatar = Document.objects.get(tags=f'{content_type.model}-{obj.id}-avatar')
        except Document.DoesNotExist:
            return None

        request = self.context.get('request')
        serializer = DocumentSerializer(
            avatar,
            many=False,
            allow_null=True,
            context={"request": request}
        )
        return serializer.data
