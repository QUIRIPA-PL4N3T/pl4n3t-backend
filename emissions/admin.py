from django.contrib import admin
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


@admin.register(EmissionFactor)
class EmissionFactorAdmin(admin.ModelAdmin):
    inlines = [GreenhouseGasEmissionInline]
    list_display = ['name', 'unit']
    search_fields = ['name']


