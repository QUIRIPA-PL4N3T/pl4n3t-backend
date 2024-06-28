from django.contrib.contenttypes.models import ContentType
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from companies.models import Company, Brand, Member, Location, EmissionsSource
from documents.models import Document
from documents.serializer import BaseDocumentSerializer
from django.utils.translation import gettext_lazy as _


class EmissionsSourceSerializer(BaseDocumentSerializer):
    class Meta:
        model = EmissionsSource
        fields = '__all__'
        read_only_fields = ['id', 'emission_source_name']


class EmissionsSourceRequestSerializer(serializers.ModelSerializer):
    documents = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    def create(self, validated_data):
        documents_data = validated_data.pop('documents', [])
        user = self.context['request'].user
        emission_source = EmissionsSource.objects.create(**validated_data)
        self.save_documents(emission_source, documents_data, user)
        return emission_source

    def update(self, instance, validated_data):
        documents_data = validated_data.pop('documents', [])
        user = self.context['request'].user
        instance = super().update(instance, validated_data)
        self.save_documents(instance, documents_data, user)
        return instance

    def save_documents(self, emission_source, documents_data, user): # noqa
        for document_data in documents_data:
            Document.objects.create(
                file=document_data,
                content_type=ContentType.objects.get_for_model(emission_source),
                object_pk=emission_source.pk,
                user_created=user
            )

    class Meta:
        model = EmissionsSource
        exclude = ['id']


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
        # Returns the readable representation of the role.
        return obj.get_role_display()

    def validate(self, data):
        company = self.context['company']
        data['company'] = company
        request = self.context.get('request')

        if self.instance is None and company:
            # Validate that the user making the request is a member of the company
            if not Member.objects.filter(company=company, user=request.user).exists():
                raise ValidationError(_("No tienes permiso para realizar esta acción."))

            # Validate company membership
            if not hasattr(company, 'membership') or not company.membership or not company.membership.is_active:
                raise ValidationError("La compañía no tiene una membresía válida.")

            # Validate the number of users allowed by the membership
            if company.membership.num_users != -1 and company.members_roles.count() >= company.membership.num_users:
                raise ValidationError("La compañía ha alcanzado el límite de usuarios permitidos por su membresía.")

            # Validate that a member with the same email address does not already exist in the company.
            if Member.objects.filter(company=company, email=data['email']).exists():
                raise ValidationError(_("Ya existe una invitación para este correo electrónico en esta compañía."))
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
            'id', 'name', 'description', 'industry', 'size', 'website',
            'geo_location', 'economic_sector', 'industry_type', 'country', 
            'address', 'postal_code', 'phone', 'state', 'city', 
            'logo_absolute_url', 'email', 'country_name', 'state_name', 
            'city_name', 'nit', 'logo', 'economic_sector_name', 
            'size_name', 'industry_type_name'
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
