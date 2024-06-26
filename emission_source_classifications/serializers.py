from rest_framework import serializers
from emissions.serializers import FactorTypeSerializer
from .models import QuantificationType, GHGScope, ISOCategory, EmissionSourceGroup, \
    CommonEquipment, CommonActivity, CommonProduct, Investment


class QuantificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuantificationType
        fields = ('id', 'name', 'code', 'description')


class GHGScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GHGScope
        fields = ('id', 'name', 'quantification_type', 'code', 'description')


class ISOCategorySerializer(serializers.ModelSerializer):
    scope_name = serializers.CharField(source='scope.name', read_only=True)

    class Meta:
        model = ISOCategory
        fields = ('id', 'name', 'code', 'scope', 'scope_name', 'description')


class EmissionSourceGroupBaseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = EmissionSourceGroup
        fields = ('id', 'name', 'description', 'icon', 'category', 'category_name',
                  'allow_inventory', 'enabled', 'form_name', 'classification')


class EmissionSourceGroupListSerializer(EmissionSourceGroupBaseSerializer):
    class Meta(EmissionSourceGroupBaseSerializer.Meta):
        pass


class EmissionSourceGroupDetailSerializer(EmissionSourceGroupBaseSerializer):
    emission_factor_type_names = serializers.StringRelatedField(source='emission_factor_types', many=True)

    class Meta(EmissionSourceGroupBaseSerializer.Meta):
        fields = EmissionSourceGroupBaseSerializer.Meta.fields + ('emission_factor_type_names',)


class CommonEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonEquipment
        fields = ('id', 'name')


class CommonActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonActivity
        fields = ('id', 'name')


class CommonProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonProduct
        fields = ('id', 'name')


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ('id', 'name')


class EmissionCalculationInputSerializer(serializers.Serializer):
    emission_source_id = serializers.IntegerField()
    consumption = serializers.FloatField()
    unit_of_measure_id = serializers.IntegerField()


class EmissionCalculationResultDetailSerializer(serializers.Serializer):
    gas_name = serializers.CharField()
    gas = serializers.CharField()
    value = serializers.FloatField()
    co2e = serializers.FloatField()
    uncertainty = serializers.FloatField()
    gwp = serializers.FloatField()


class EmissionCalculationResultSerializer(serializers.Serializer):
    component = serializers.CharField()
    co2e = serializers.FloatField()
    results = EmissionCalculationResultDetailSerializer(many=True)

