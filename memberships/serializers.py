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


class PhoneSerializer(serializers.Serializer):
    area_code = serializers.CharField(max_length=10)
    number = serializers.CharField(max_length=20)


class IdentificationSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=10)
    number = serializers.CharField(max_length=20)


class AddressSerializer(serializers.Serializer):
    street_name = serializers.CharField(max_length=100)
    street_number = serializers.IntegerField()
    zip_code = serializers.CharField(max_length=20)


class PayerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = PhoneSerializer()
    identification = IdentificationSerializer()
    address = AddressSerializer()


class BackUrlsSerializer(serializers.Serializer):
    success = serializers.URLField()
    failure = serializers.URLField()
    pending = serializers.URLField()


class PurchaseSerializer(serializers.Serializer):
    payer = PayerSerializer()
    back_urls = BackUrlsSerializer()


class PreferenceRequestSerializer(serializers.Serializer):
    init_point = serializers.URLField()
    preference_id = serializers.CharField()
    items = serializers.ListField()
    payer = serializers.DictField()
    back_urls = serializers.DictField()
    auto_return = serializers.CharField()


class PaymentMethodsSerializer(serializers.Serializer):
    default_card_id = serializers.CharField(allow_null=True, required=False)
    default_payment_method_id = serializers.CharField(allow_null=True, required=False)
    excluded_payment_methods = serializers.ListField(child=serializers.DictField())
    excluded_payment_types = serializers.ListField(child=serializers.DictField())
    installments = serializers.IntegerField(allow_null=True, required=False)
    default_installments = serializers.IntegerField(allow_null=True, required=False)


class PreferenceResponseSerializer(serializers.Serializer):
    additional_info = serializers.CharField(allow_blank=True, required=False)
    auto_return = serializers.CharField()
    back_urls = BackUrlsSerializer()
    binary_mode = serializers.BooleanField()
    client_id = serializers.CharField()
    collector_id = serializers.CharField()
    coupon_code = serializers.CharField(allow_null=True, required=False)
    coupon_labels = serializers.CharField(allow_null=True, required=False)
    date_created = serializers.DateTimeField()
    date_of_expiration = serializers.DateTimeField(allow_null=True, required=False)
    expiration_date_from = serializers.DateTimeField(allow_null=True, required=False)
    expiration_date_to = serializers.DateTimeField(allow_null=True, required=False)
    expires = serializers.BooleanField()
    external_reference = serializers.CharField(allow_blank=True, required=False)
    id = serializers.CharField()
    init_point = serializers.URLField()
    internal_metadata = serializers.CharField(allow_null=True, required=False)
    marketplace = serializers.CharField()
    marketplace_fee = serializers.IntegerField()
    metadata = serializers.DictField()
    notification_url = serializers.CharField(allow_null=True, required=False)
    operation_type = serializers.CharField()
    payer = PayerSerializer()
    payment_methods = PaymentMethodsSerializer()
    processing_modes = serializers.CharField(allow_null=True, required=False)
    product_id = serializers.CharField(allow_null=True, required=False)
    redirect_urls = BackUrlsSerializer()
    sandbox_init_point = serializers.URLField()
    site_id = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True, required=False)
    last_updated = serializers.DateTimeField(allow_null=True, required=False)
