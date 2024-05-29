from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.forms import ModelForm
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from emissions.models import GreenhouseGas, EmissionFactor, GreenhouseGasEmission, FactorType, SourceType, \
    EmissionFactorComponent
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


class EmissionFactorComponentInlineForm(ModelForm):
    class Meta:
        model = EmissionFactorComponent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs and kwargs['instance'].pk:
            emission_factor = kwargs['instance'].emission_factor
            self.fields['component_factor'].queryset = EmissionFactor.objects.filter(
                factor_type=emission_factor.factor_type,
                source_type=emission_factor.source_type
            ).exclude(id=emission_factor.id)
        else:
            # Esto es una nueva instancia; el queryset puede ser configurado después de guardar el formulario
            self.fields['component_factor'].queryset = EmissionFactor.objects.none()


class EmissionFactorComponentInline(admin.TabularInline):
    model = EmissionFactorComponent
    form = EmissionFactorComponentInlineForm
    extra = 1
    fk_name = 'emission_factor'

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        class CustomFormSet(formset):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # Filtra el queryset para component_factor
                for form in self.forms:
                    if 'component_factor' in form.fields:
                        if obj:
                            form.fields['component_factor'].queryset = EmissionFactor.objects.filter(
                                factor_type=obj.factor_type,
                                source_type=obj.source_type
                            ).exclude(id=obj.id)
                        else:
                            form.fields['component_factor'].queryset = EmissionFactor.objects.none()

        return CustomFormSet


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
        fields = ('id', 'name', 'description', 'observations', 'factor_type', 'source_type',
                  'valid_from', 'valid_until', 'unit')
        export_order = ('id', 'name', 'description', 'observations', 'factor_type', 'source_type',
                        'valid_from', 'valid_until', 'unit')


@admin.register(EmissionFactor)
class EmissionFactorAdmin(ImportExportModelAdmin):
    resource_class = EmissionFactorResource
    list_filter = ['source_type', 'factor_type']
    inlines = [EmissionFactorComponentInline, GreenhouseGasEmissionInline]
    list_display = ['name', 'source_type', 'unit', 'measure_type', 'factor_type',]
    list_editable = ['measure_type', 'measure_type']
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        obj.clean()  # Validación antes de guardar
        super().save_model(request, obj, form, change)

class GreenhouseGasEmissionResource(resources.ModelResource):

    emission_factor_id = fields.Field(
        column_name='emission_factor_id',
        attribute='emission_factor',
        widget=ForeignKeyWidget(EmissionFactor, 'id'))

    emission_factor = fields.Field(
        column_name='emission_factor',
        attribute='emission_factor',
        widget=ForeignKeyWidget(EmissionFactor, 'name'))

    description = fields.Field(
        column_name='description',
        attribute='emission_factor',
        widget=ForeignKeyWidget(EmissionFactor, 'description'))

    observations = fields.Field(
        column_name='observations',
        attribute='emission_factor',
        widget=ForeignKeyWidget(EmissionFactor, 'observations'))

    factor_type = fields.Field(
        column_name='factor_type',
        attribute='emission_factor__factor_type__name',
        readonly=True)

    source_type = fields.Field(
        column_name='source_type',
        attribute='emission_factor__source_type__name',
        readonly=True)

    valid_from = fields.Field(
        column_name='valid_from',
        attribute='emission_factor__valid_from',
        readonly=True)

    valid_until = fields.Field(
        column_name='source_type',
        attribute='emission_factor__valid_until',
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
        fields = ('id', 'emission_factor_id', 'emission_factor', 'description', 'observations', 'factor_type',
                  'source_type', 'valid_from', 'valid_until', 'greenhouse_gas', 'value', 'unit', 'bibliographic_source',
                  'percentage_uncertainty', 'maximum_allowed_amount')
        export_order = fields


@admin.register(GreenhouseGasEmission)
class GreenhouseGasEmissionAdmin(ImportExportModelAdmin):
    resource_class = GreenhouseGasEmissionResource
    list_display = ['emission_factor', 'greenhouse_gas', 'unit', 'value']
    search_fields = ['emission_factor__name', 'greenhouse_gas__name']
    list_filter = ['emission_factor__source_type', 'emission_factor__factor_type']
