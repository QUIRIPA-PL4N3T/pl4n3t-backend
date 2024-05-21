from rest_framework import serializers
from main.models import Configuration, State, City, DocumentType, UnitOfMeasure, EconomicSector, IndustryType, \
    LocationType, Country


class ConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = ['key', 'value', 'company']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if rep['key'].endswith('_LIST'):
            rep['value'] = rep['value'].replace('\r', '').replace('\n', '')
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


class UnitOfMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOfMeasure
        fields = [
             'id', 'name', 'slug', 'symbol', 'measure_type', 'name_standard_unit',
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
