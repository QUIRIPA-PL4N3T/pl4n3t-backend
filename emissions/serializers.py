from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from companies.serializers import EmissionsSourceSerializer
from documents.serializer import BaseDocumentSerializer
from emissions.models import GreenhouseGas, SourceType, FactorType, EmissionFactor, GreenhouseGasEmission, \
     EmissionFactorComponent, EmissionGasDetail, EmissionResult, TotalEmissionGas, Co2ByComponent
from main.serializer import UnitOfMeasureSerializer

# MAIN GAS ID'S
CO_GAS_ID = 1
HC_GAS_ID = 2
CH4_GAS_ID = 3
N2O_GAS_ID = 4
HFCS_GAS_ID = 5
PFCS_GAS_ID = 6
SF6_GAS_ID = 7
CFCS_GAS_ID = 8
CO2_GAS_ID = 9


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
        fields = ['greenhouse_gas', 'value', 'co2e', 'emission_factor']


class EmissionResultSerializer(BaseDocumentSerializer):
    gas_details = EmissionGasDetailSerializer(many=True)

    class Meta:
        model = EmissionResult
        fields = [
            'id',
            'name',
            'date',
            'usage',
            'unit',
            'total_co2e',
            'gas_details',
            'documents',
            'emission_source',
            'location',
            'user_created',
            'month',
            'year'
        ]
        read_only_fields = ['id', 'user_created']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request is not None:
            validated_data['user_created'] = request.user

        gas_details_data = validated_data.pop('gas_details')
        emission_result = EmissionResult.objects.create(**validated_data)
        for gas_detail_data in gas_details_data:
            EmissionGasDetail.objects.create(emission_result=emission_result, **gas_detail_data)

        emission_result.calculate_totals()
        return emission_result


class EmissionGasDetailFullSerializer(serializers.ModelSerializer):
    greenhouse_gas = GreenhouseGasSerializer()

    class Meta:
        model = EmissionGasDetail
        fields = ['greenhouse_gas', 'value', 'co2e', 'emission_factor']


class TotalEmissionGasSerializer(serializers.ModelSerializer):
    greenhouse_gas = GreenhouseGasSerializer()

    class Meta:
        model = TotalEmissionGas
        fields = ['greenhouse_gas', 'value', 'co2e']


class Co2ByComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Co2ByComponent
        fields = ['emission_factor', 'co2e']


class EmissionResultListSerializer(serializers.ModelSerializer):
    co2 = serializers.SerializerMethodField()
    hc4 = serializers.SerializerMethodField()
    n2o = serializers.SerializerMethodField()
    co = serializers.SerializerMethodField()
    hc = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    source_name = serializers.SerializerMethodField()
    unit_symbol = serializers.SerializerMethodField()
    total_co2e = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_co2(self, obj): # noqa
        return obj.get_total_gas_value(CO2_GAS_ID)

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_hc4(self, obj): # noqa
        return obj.get_total_gas_value(CH4_GAS_ID)

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_n2o(self, obj): # noqa
        return obj.get_total_gas_value(N2O_GAS_ID)

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_co(self, obj): # noqa
        return obj.get_total_gas_value(CO_GAS_ID)

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_hc(self, obj): # noqa
        return obj.get_total_gas_value(HC_GAS_ID)

    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_total_co2e(self, obj):
        return round(obj.total_co2e)

    @extend_schema_field(OpenApiTypes.STR)
    def get_month(self, obj: EmissionResult):
        return obj.get_month_display()

    @extend_schema_field(OpenApiTypes.STR)
    def get_unit_symbol(self, obj: EmissionResult):
        return obj.unit.symbol

    @extend_schema_field(OpenApiTypes.STR)
    def get_source_name(self, obj: EmissionResult):
        return obj.emission_source.emission_source_name

    class Meta:
        model = EmissionResult
        fields = ['id', 'name', 'date', 'usage', 'month', 'year',
                  'unit', 'total_co2e', 'co2', 'hc4', 'n2o', 'co', 'hc',
                  'unit_symbol', 'source_name']


class EmissionResultDetailSerializer(BaseDocumentSerializer):
    gas_details = EmissionGasDetailFullSerializer(many=True)
    total_emissions_gas = TotalEmissionGasSerializer(many=True)
    co2_by_component = Co2ByComponentSerializer(many=True)
    emission_source = EmissionsSourceSerializer()

    class Meta:
        model = EmissionResult
        fields = [
            'id',
            'name',
            'date',
            'usage',
            'unit',
            'total_co2e',
            'gas_details',
            'total_emissions_gas',
            'co2_by_component',
            'emission_source',
            'location',
            'user_created',
            'month',
            'year',
            'documents'
        ]
