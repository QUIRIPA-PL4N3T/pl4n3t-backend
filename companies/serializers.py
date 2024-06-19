from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from companies.models import Company, Brand, Member, Location, EmissionsSource, EmissionsSourceMonthEntry
from documents.serializer import BaseDocumentSerializer
from memberships.serializers import CompanyMembershipSerializer
from django.utils.translation import gettext_lazy as _


class EmissionsSourceSerializer(BaseDocumentSerializer):
    class Meta:
        model = EmissionsSource
        fields = (
            'id', 'name', 'code', 'description', 'location', 'image', 'group',
            'source_type', 'geo_location', 'factor_type', 'emission_factor', 'emission_factor_unit',
            'vehicle_type', 'vehicle_load', 'vehicle_fuel', 'vehicle_capacity',
            'vehicle_efficiency', 'vehicle_efficiency_unit', 'electricity_supplier',
            'electricity_source', 'electricity_efficiency', 'electricity_efficiency_unit',
            'know_type_electricity_generation_source', 'waste_management',
            'leased_assets_type', 'leased_assets_durations', 'leased_assets_duration_unit',
            'fuel_store', 'fuel_management', 'exist_steam_specific_factor', 'activity_name',
            'equipment_name', 'origin', 'energy_efficiency_value', 'energy_efficiency_unit',
            'service_life', 'service_life_unit', 'good_and_service_acquired_type',
            'acquired_service', 'supplier_name', 'ghg_emission_are_recorded', 'waste_type',
            'waste_classification', 'investment_type', 'refrigerant_capacity',
            'refrigerant_capacity_unit', 'has_refrigerant_leaks', 'has_refrigerant_conversions',
            'final_disposal_of_refrigerants', 'support_actions_refrigerant_equipment',
            'product_name', 'documents', 'emission_source_name', 'group_name', 'waste_management_data',
            'product_operation_requirements', 'units_sold', 'units_sold_period'
        )
        read_only_fields = ['id', 'emission_source_name']


class EmissionsSourceMonthEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionsSourceMonthEntry
        fields = ('id', 'register_date', 'emission_agent', 'month', 'emission', 'unit')


class BrandSerializer(serializers.ModelSerializer):

    def validate(self, data):
        company = data.get('company')
        if self.instance is None and company:
            if not company.membership or not company.membership.is_active:
                raise serializers.ValidationError("La compañía no tiene una membresía válida.")

            if company.membership.num_brands != -1 and company.brands.count() >= company.membership.num_brands:
                raise serializers.ValidationError(
                    "La compañía ha alcanzado el límite de marcas permitidas por su membresía.")
        return data

    class Meta:
        model = Brand
        fields = ('id', 'company', 'name', 'description', 'logo', 'logo_absolute_url')
        extra_kwargs = {
            'logo': {'write_only': True}
        }


class MemberSerializer(serializers.ModelSerializer):
    role_description = serializers.SerializerMethodField(read_only=True)
    company = serializers.HiddenField(default=None)

    @extend_schema_field(OpenApiTypes.STR)
    def get_role_description(self, obj: Member):
        # Devuelve la representación legible del rol.
        return obj.get_role_display()

    def validate(self, data):
        company = self.context['company']
        data['company'] = company
        request = self.context.get('request')

        if self.instance is None and company:
            # Validar que el usuario que realiza la petición es miembro de la compañía
            if not Member.objects.filter(company=company, user=request.user).exists():
                raise ValidationError(_("No tienes permiso para realizar esta acción."))

            # Validar la membresía de la compañía
            if not hasattr(company, 'membership') or not company.membership or not company.membership.is_active:
                raise ValidationError("La compañía no tiene una membresía válida.")

            # Validar el número de usuarios permitido por la membresía
            if company.membership.num_users != -1 and company.members_roles.count() >= company.membership.num_users:
                raise ValidationError("La compañía ha alcanzado el límite de usuarios permitidos por su membresía.")
        return data

    class Meta:
        model = Member
        fields = ('id', 'company', 'email', 'role', 'role_description', 'status')
        read_only_fields = ['id', 'role_description']


class LocationSerializer(serializers.ModelSerializer):
    emission_sources = EmissionsSourceSerializer(many=True, read_only=True)

    def validate(self, data):
        company = data.get('company')
        if self.instance is None and company:
            if not company.membership or not company.membership.is_active:
                raise serializers.ValidationError("La compañía no tiene una membresía válida.")

            if company.membership.num_locations != -1 and company.locations.count() >= company.membership.num_locations:
                raise serializers.ValidationError(
                    "La compañía ha alcanzado el límite de Sedes permitidas por su membresía.")
        return data

    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'phone', 'email', 'country', 'state', 'city',
                  'zip_code',  'company', 'geo_location', 'brand', 'location_type',
                  'employees', 'emission_sources')


class CompanySerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    members_roles = MemberSerializer(many=True, read_only=True)
    brands = BrandSerializer(many=True, read_only=True)
    membership = CompanyMembershipSerializer(read_only=True)

    country_name = serializers.SerializerMethodField(read_only=True)
    state_name = serializers.SerializerMethodField(read_only=True)
    city_name = serializers.SerializerMethodField(read_only=True)
    economic_sector_name = serializers.SerializerMethodField(read_only=True)
    industry_type_name = serializers.SerializerMethodField(read_only=True)
    size_name = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(OpenApiTypes.STR)
    def get_country_name(self, obj: Company):  # noqa
        return obj.country.name if obj.country else ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_state_name(self, obj: Company):  # noqa
        return obj.state.name if obj.state else ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_city_name(self, obj: Company):  # noqa
        return obj.city.name if obj.city else ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_economic_sector_name(self, obj: Company):  # noqa
        return obj.economic_sector.name if obj.economic_sector else ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_industry_type_name(self, obj: Company):  # noqa
        return obj.industry_type.name if obj.industry_type else ''

    @extend_schema_field(OpenApiTypes.STR)
    def get_size_name(self, obj: Company):  # noqa
        return obj.get_size_display()

    class Meta:
        model = Company
        fields = (
            'id', 'name', 'description', 'industry', 'size', 'locations',
            'website', 'geo_location', 'economic_sector', 'industry_type',
            'members_roles', 'brands', 'country', 'address', 'postal_code',
            'phone', 'state', 'city', 'logo_absolute_url', 'email', 'country_name',
            'state_name', 'city_name', 'nit', 'logo', 'economic_sector_name',
            'size_name', 'industry_type_name', 'economic_sector_name', 'membership'
        )


class CompanyLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('logo',)


class GasEmissionSummarySerializer(serializers.Serializer):
    gas_name = serializers.CharField()
    total_value = serializers.FloatField()
    percentage_change = serializers.FloatField()


class EmissionSourceSummarySerializer(serializers.Serializer):
    source_type = serializers.CharField()
    value = serializers.FloatField()


class GEISummarySerializer(serializers.Serializer):
    category = serializers.CharField()
    percentage = serializers.FloatField()


class DashboardDataSerializer(serializers.Serializer):
    gas_emissions = GasEmissionSummarySerializer(many=True)
    emission_sources = EmissionSourceSummarySerializer(many=True)
    gei_distribution = GEISummarySerializer(many=True)
    total_emissions = serializers.FloatField()
