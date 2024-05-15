from rest_framework import serializers
from memberships.models import Membership, CompanyMembership


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = [
            'id', 'name', 'membership_type', 'price', 'duration', 'description', 'benefits',
            'num_brands', 'num_locations', 'num_users', 'emission_sources', 'footprint_types',
            'liquidation_options', 'analysis_tools', 'basic_support', 'storage_capacity',
            'tutorials', 'webinars', 'general_support', 'dedicated_support', 'custom_api_access'
        ]


class CompanyMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMembership
        fields = ['id', 'company', 'membership', 'start_date', 'end_date']


class PurchaseMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()
    payment_method = serializers.CharField(max_length=50)
