from rest_framework import serializers
from companies.models import Company, Brand, CompanyUser, Location, EmissionsSource, EmissionsSourceMonthEntry


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'industry', 'size',
                  'website', 'geo_location', 'economic_sector', 'industry_type')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'company', 'name', 'description', 'logo')


class CompanyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUser
        fields = ('id', 'company', 'user')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'city', 'country', 'zip_code',
                  'company', 'geo_location', 'brand', 'location_type')


class EmissionsSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionsSource
        fields = ('id', 'name', 'code', 'description', 'location', 'image',
                  'group', 'source_type', 'geo_location')


class EmissionsSourceMonthEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionsSourceMonthEntry
        fields = ('id', 'register_date', 'emission_agent', 'month', 'emission', 'unit')
