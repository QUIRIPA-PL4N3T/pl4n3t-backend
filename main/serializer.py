from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from main.models import Configuration, State, City, DocumentType, UnitOfMeasure, EconomicSector, IndustryType, \
    LocationType, Country


class OptionSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ['key', 'value', 'company']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if rep['key'].endswith('_LIST'):
            rep['value'] = rep['value'].replace('\r', '').replace('\n', '')
        return rep


class ConfigurationDetailSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Configuration
        fields = ['key', 'options', 'company']

    @extend_schema_field(OptionSerializer(many=True))
    def get_options(self, obj):
        values = obj.value.replace('\r', '').replace('\n', '').split(',')
        return [{'value': value.strip(), 'label': value.strip()} for value in values]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['key'] = [rep['key']]  # Asegura que 'key' siempre sea un arreglo
        return rep


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'iso_code', 'slug')


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'dane_code', 'geonames_code', 'slug']


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id', 'state', 'name', 'dane_code', 'slug', 'coords_lat', 'coords_long', 'geo_location']


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'code']


class MeasureTypeSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(OpenApiTypes.STR)
    def get_group(self, instance):
        return instance.get_measure_type_display()

    class Meta:
        model = UnitOfMeasure
        fields = [
             'id', 'name', 'group', 'slug', 'symbol', 'measure_type', 'name_standard_unit',
            'scale_to_standard_unit', 'offset_to_standard_unit', 'formula', 'is_gei_unit'
        ]


class EconomicSectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EconomicSector
        fields = ['id', 'name']


class IndustryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryType
        fields = ['id', 'name']


class LocationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationType
        fields = ['id', 'name']
