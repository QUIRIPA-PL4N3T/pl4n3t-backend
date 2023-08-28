from rest_framework import serializers
from companies.models import Company, Brand, Member, Location, EmissionsSource, EmissionsSourceMonthEntry


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'company', 'name', 'description', 'logo')


class MemberSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    role_description = serializers.SerializerMethodField()

    def get_role_description(self, obj: Member): # noqa
        # Devuelve la representación legible del rol.
        return obj.get_role_display()

    class Meta:
        model = Member
        fields = ('id', 'company', 'user_email', 'role', 'role_description')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'city', 'country', 'zip_code',
                  'company', 'geo_location', 'brand', 'location_type')


class CompanySerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    members_roles = MemberSerializer(many=True, read_only=True)
    brands = BrandSerializer(many=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'industry', 'size', 'locations',
                  'website', 'geo_location', 'economic_sector', 'industry_type',
                  'members_roles', 'brands', 'country')


class EmissionsSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionsSource
        fields = ('id', 'name', 'code', 'description', 'location', 'image',
                  'group', 'source_type', 'geo_location')


class EmissionsSourceMonthEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionsSourceMonthEntry
        fields = ('id', 'register_date', 'emission_agent', 'month', 'emission', 'unit')
