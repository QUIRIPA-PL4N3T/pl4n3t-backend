from rest_framework import serializers
from emissions.models import GreenhouseGas, SourceType, FactorType, EmissionFactor, GreenhouseGasEmission


class GreenhouseGasSerializer(serializers.ModelSerializer):
    class Meta:
        model = GreenhouseGas
        fields = ('id', 'name', 'acronym', 'kg_co2_equivalence', 'pcg_min', 'pcg_max', 'lifespan_in_years')


class SourceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceType
        fields = ('id', 'name', 'description')


class FactorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorType
        fields = ('id', 'name', 'description')


class EmissionFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionFactor
        fields = ('id', 'name', 'description', 'factor_type', 'source_type', 'unit')


class GreenhouseGasEmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GreenhouseGasEmission
        fields = ('id', 'greenhouse_gas', 'unit', 'emission_factor', 'value',
                  'bibliographic_source', 'percentage_uncertainty', 'maximum_allowed_amount')
