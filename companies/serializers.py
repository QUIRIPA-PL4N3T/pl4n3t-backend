from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from companies.models import Company, Brand, Member, Location, EmissionsSource, EmissionsSourceMonthEntry
from documents.serializer import BaseDocumentSerializer


class EmissionsSourceSerializer(BaseDocumentSerializer):
    class Meta:
        model = EmissionsSource
        fields = ('id', 'name', 'code', 'description', 'location', 'image', 'group',
                  'source_type', 'geo_location', 'factor_type', 'emission_factor',
                  'vehicle_type', 'vehicle_load', 'vehicle_fuel', 'vehicle_capacity',
                  'vehicle_efficiency', 'vehicle_efficiency_unit', 'electricity_supplier',
                  'electricity_source', 'electricity_efficiency', 'electricity_efficiency_unit',
                  'documents')


class EmissionsSourceMonthEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionsSourceMonthEntry
        fields = ('id', 'register_date', 'emission_agent', 'month', 'emission', 'unit')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'company', 'name', 'description', 'logo', 'logo_absolute_url')
        extra_kwargs = {
            'logo': {'write_only': True}
        }


class MemberSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    role_description = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_role_description(self, obj: Member): # noqa
        # Devuelve la representación legible del rol.
        return obj.get_role_display()

    class Meta:
        model = Member
        fields = ('id', 'company', 'user_email', 'role', 'role_description')


class LocationSerializer(serializers.ModelSerializer):
    emission_source_locations = EmissionsSourceSerializer(many=True, read_only=True)

    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'phone', 'email', 'country', 'state', 'city',
                  'zip_code',  'company', 'geo_location', 'brand', 'location_type',
                  'employees', 'emission_source_locations')


class CompanySerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    members_roles = MemberSerializer(many=True, read_only=True)
    brands = BrandSerializer(many=True, read_only=True)

    country_name = serializers.SerializerMethodField(read_only=True)
    state_name = serializers.SerializerMethodField(read_only=True)
    city_name = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(OpenApiTypes.STR)
    def get_country_name(self, obj:Company): # noqa
        return obj.country.name if obj.country else ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_state_name(self, obj:Company): # noqa
        return obj.state.name if obj.state else ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_city_name(self, obj:Company): # noqa
        return obj.city.name if obj.city else ''

    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'industry', 'size', 'locations',
                  'website', 'geo_location', 'economic_sector', 'industry_type',
                  'members_roles', 'brands', 'country', 'address', 'postal_code',
                  'phone', 'state', 'city', 'logo_absolute_url', 'email', 'country_name',
                  'state_name', 'city_name', 'nit', 'logo')


class CompanyLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('logo',)
