from rest_framework import serializers
from companies.serializers import EmissionsSourceRequestSerializer
from django.contrib.gis.db import models as gis_models


def generate_schema_for_emission_source():
    serializer = EmissionsSourceRequestSerializer()
    properties = {}

    for field_name, field in serializer.fields.items():
        if isinstance(field, serializers.CharField):
            properties[field_name] = {'type': 'string'}
        elif isinstance(field, serializers.FloatField):
            properties[field_name] = {'type': 'number'}
        elif isinstance(field, serializers.IntegerField):
            properties[field_name] = {'type': 'integer'}
        elif isinstance(field, serializers.BooleanField):
            properties[field_name] = {'type': 'boolean'}
        elif isinstance(field, serializers.FileField):
            properties[field_name] = {'type': 'string', 'format': 'binary'}
        elif isinstance(field, serializers.ListField) and isinstance(field.child, serializers.FileField):
            properties[field_name] = {'type': 'array', 'items': {'type': 'string', 'format': 'binary'}}
        elif isinstance(field, gis_models.PointField):
            properties[field_name] = {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string', 'enum': ['Point']},
                    'coordinates': {
                        'type': 'array',
                        'items': {'type': 'number'}
                    }
                }
            }
        else:
            properties[field_name] = {'type': 'string'}

    return {
        'multipart/form-data': {
            'type': 'object',
            'properties': properties
        }
    }
