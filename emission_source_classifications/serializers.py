from rest_framework import serializers

from emissions.serializers import FactorTypeSerializer
from .models import QuantificationType, GHGScope, ISOCategory, EmissionSourceGroup


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


class EmissionSourceGroupSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    emission_factor_type_names = serializers.StringRelatedField(source='emission_factor_types', many=True)
    emission_factor_types = FactorTypeSerializer(read_only=True, many=True)

    class Meta:
        model = EmissionSourceGroup
        fields = ('id', 'name', 'description', 'icon', 'category', 'category_name',
                  'emission_factor_types', 'emission_factor_type_names', 'emission_factor_types',
                  'allow_inventory', 'classification')
