from rest_framework import serializers
from .models import ReportTemplate, CompanyTemplate, Report


class ReportTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = ['id', 'name', 'version', 'creation_date']


class ReportTemplateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = '__all__'


class CompanyTemplateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyTemplate
        fields = ['id', 'name', 'version', 'creation_date', 'company']


class CompanyTemplateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyTemplate
        fields = '__all__'


class ReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'name', 'version', 'creation_date', 'period', 'is_finalized']


class ReportDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
