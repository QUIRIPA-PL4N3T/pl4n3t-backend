from rest_framework import serializers
from memberships.models import Membership, CompanyMembership


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'name', 'membership_type', 'price', 'duration', 'description', 'benefits']


class CompanyMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMembership
        fields = ['id', 'company', 'membership', 'start_date', 'end_date']


class PurchaseMemberSerializer(serializers.Serializer):
    email = serializers.EmailField()
    payment_method = serializers.CharField(max_length=50)
