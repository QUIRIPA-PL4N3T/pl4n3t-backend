from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from emissions.models import GreenhouseGas, EmissionFactor, GreenhouseGasEmission, FactorType, SourceType
from import_export import fields
from import_export.widgets import ForeignKeyWidget
from main.models import UnitOfMeasure


# Emission factor classifications
@admin.register(GreenhouseGas)
class GreenhouseGasAdmin(admin.ModelAdmin):
    list_display = ['name', 'acronym', 'kg_co2_equivalence', 'pcg_min', 'pcg_max']


@admin.register(FactorType)
class FactorTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(SourceType)
class SourceTypeAdmin(admin.ModelAdmin):
    pass


class GreenhouseGasEmissionInline(admin.TabularInline):
    model = GreenhouseGasEmission
    extra = 1


class EmissionFactorResource(resources.ModelResource):
    factor_type = fields.Field(
        column_name='factor_type',
        attribute='factor_type',
        widget=ForeignKeyWidget(FactorType, 'name'))

    source_type = fields.Field(
        column_name='source_type',
        attribute='source_type',
        widget=ForeignKeyWidget(SourceType, 'name'))

    unit = fields.Field(
        column_name='unit',
        attribute='unit',
        widget=ForeignKeyWidget(UnitOfMeasure, 'name'))

    greenhouse_gas = fields.Field(
        column_name='greenhouse_gas',
        attribute='greenhouse_gas',
        widget=ForeignKeyWidget(GreenhouseGas, 'name'))

    def before_import_row(self, row, **kwargs):
        greenhouse_gas_name = row.get('greenhouse_gas')
        if greenhouse_gas_name:
            try:
                greenhouse_gas = GreenhouseGas.objects.get(name=greenhouse_gas_name)
                row['greenhouse_gas'] = greenhouse_gas.pk
            except GreenhouseGas.DoesNotExist:
                raise ValidationError(f"Greenhouse gas '{greenhouse_gas_name}' does not exist.")

    def before_export(self, queryset, *args, **kwargs):
        queryset = super().before_export(queryset, *args, **kwargs)
        if queryset is not None:
            greenhouse_gas_prefetch = Prefetch('greenhouse_emission_gases', queryset=GreenhouseGas.objects.all())
            queryset = queryset.prefetch_related(greenhouse_gas_prefetch)
        return queryset

    class Meta:
        model = EmissionFactor
        fields = ('id', 'name', 'description', 'factor_type', 'source_type', 'unit', 'greenhouse_gas')
        export_order = ('id', 'name', 'description', 'factor_type', 'source_type', 'unit', 'greenhouse_gas')


@admin.register(EmissionFactor)
class EmissionFactorAdmin(ImportExportModelAdmin):
    resource_class = EmissionFactorResource
    list_filter = ['source_type', 'factor_type']
    inlines = [GreenhouseGasEmissionInline]
    list_display = ['name', 'source_type', 'unit', 'measure_type', 'factor_type',]
    list_editable = ['measure_type', 'measure_type']
    search_fields = ['name']


class GreenhouseGasEmissionResource(resources.ModelResource):

    emission_factor_id = fields.Field(
        column_name='emission_factor_id',
        attribute='emission_factor',
        widget=ForeignKeyWidget(EmissionFactor, 'id'))

    emission_factor = fields.Field(
        column_name='emission_factor',
        attribute='emission_factor',
        widget=ForeignKeyWidget(EmissionFactor, 'name'))

    factor_type = fields.Field(
        column_name='factor_type',
        attribute='emission_factor__factor_type__name',
        readonly=True)

    source_type = fields.Field(
        column_name='source_type',
        attribute='emission_factor__source_type__name',
        readonly=True)

    greenhouse_gas = fields.Field(
        column_name='greenhouse_gas',
        attribute='greenhouse_gas',
        widget=ForeignKeyWidget(GreenhouseGas, 'name'))

    unit = fields.Field(
        column_name='unit',
        attribute='unit',
        widget=ForeignKeyWidget(UnitOfMeasure, 'name'))

    def get_queryset(self):
        return super().get_queryset().order_by('emission_factor__id', 'emission_factor__name')

    class Meta:
        model = GreenhouseGasEmission
        fields = ('emission_factor_id', 'emission_factor', 'factor_type', 'source_type', 'greenhouse_gas',
                  'unit', 'value', 'bibliographic_source', 'percentage_uncertainty', 'maximum_allowed_amount')
        export_order = fields


@admin.register(GreenhouseGasEmission)
class GreenhouseGasEmissionAdmin(ImportExportModelAdmin):
    resource_class = GreenhouseGasEmissionResource
    list_display = ['emission_factor', 'greenhouse_gas', 'unit', 'value']
    search_fields = ['emission_factor__name', 'greenhouse_gas__name']
