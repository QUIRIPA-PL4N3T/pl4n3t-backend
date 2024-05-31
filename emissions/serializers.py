from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from emissions.models import GreenhouseGas, SourceType, FactorType, EmissionFactor, GreenhouseGasEmission, \
    EmissionFactorComponent, EmissionGasDetail, EmissionResult
from main.serializer import UnitOfMeasureSerializer


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


class GreenhouseGasEmissionSerializer(serializers.ModelSerializer):
    greenhouse_gas = GreenhouseGasSerializer()
    unit = UnitOfMeasureSerializer()

    class Meta:
        model = GreenhouseGasEmission
        fields = ('id', 'greenhouse_gas', 'unit', 'emission_factor', 'value',
                  'bibliographic_source', 'percentage_uncertainty', 'maximum_allowed_amount')


class EmissionFactorComponentSerializer(serializers.ModelSerializer):
    greenhouse_emission_gases = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()

    @extend_schema_field(GreenhouseGasEmissionSerializer(many=True))
    def get_greenhouse_emission_gases(self, obj):
        return GreenhouseGasEmissionSerializer(obj.component_factor.greenhouse_emission_gases, many=True).data

    @extend_schema_field(UnitOfMeasureSerializer)
    def get_unit(self, obj):
        return UnitOfMeasureSerializer(obj.component_factor.unit).data

    class Meta:
        model = EmissionFactorComponent
        fields = ('id', 'component_factor', 'application_percentage', 'component_name', 'unit',
                  'greenhouse_emission_gases')


class EmissionFactorSerializer(serializers.ModelSerializer):
    greenhouse_emission_gases = GreenhouseGasEmissionSerializer(many=True)
    components = EmissionFactorComponentSerializer(many=True, read_only=True)
    factor_type = FactorTypeSerializer()
    source_type = SourceTypeSerializer()
    unit = UnitOfMeasureSerializer()

    class Meta:
        model = EmissionFactor
        fields = ('id', 'name', 'description', 'factor_type', 'source_type', 'unit',
                  'greenhouse_emission_gases', 'measure_type', 'components', 'application_percentage')


class EmissionFactorListSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmissionFactor
        fields = ('id', 'name', 'description', 'factor_type', 'source_type',
                  'unit', 'measure_type')


class EmissionGasDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionGasDetail
        fields = ['greenhouse_gas', 'value', 'co2e']


class EmissionResultSerializer(serializers.ModelSerializer):
    gas_details = EmissionGasDetailSerializer(many=True)

    class Meta:
        model = EmissionResult
        fields = ['name', 'date', 'usage', 'unit', 'total_co2e', 'gas_details']

    def create(self, validated_data):
        gas_details_data = validated_data.pop('gas_details')
        emission_result = EmissionResult.objects.create(**validated_data)
        for gas_detail_data in gas_details_data:
            EmissionGasDetail.objects.create(emission_result=emission_result, **gas_detail_data)
        return emission_result
