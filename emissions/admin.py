from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from emissions.models import GreenhouseGas, EmissionFactor, GreenhouseGasEmission, FactorType, SourceType
from django.utils.translation import gettext_lazy as _


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
    class Meta:
        model = EmissionFactor
        fields = ('id', 'name', 'description', 'factor_type', 'source_type', 'unit')


@admin.register(EmissionFactor)
class EmissionFactorAdmin(ImportExportModelAdmin):
    resource_class = EmissionFactorResource
    list_filter = ['source_type', 'factor_type']
    inlines = [GreenhouseGasEmissionInline]
    list_display = ['name', 'source_type', 'unit', 'factor_type']
    search_fields = ['name']


