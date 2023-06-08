from django.contrib import admin
from emissions.models import GreenhouseGas, EmissionCategory, EmissionAgent, UnitGreenhouseGasByAgentEmission, \
    EmissionFactor


@admin.register(GreenhouseGas)
class GreenhouseGasAdmin(admin.ModelAdmin):
    list_display = ['name', 'acronym', 'kg_co2_equivalence', 'pcg_min', 'pcg_max']


@admin.register(EmissionFactor)
class EmissionFactorAdmin(admin.ModelAdmin):
    pass


@admin.register(EmissionCategory)
class EmissionCategoryAdmin(admin.ModelAdmin):
    pass


class UnitGreenhouseGasByAgentEmissionInline(admin.TabularInline):
    model = UnitGreenhouseGasByAgentEmission
    extra = 1


@admin.register(EmissionAgent)
class EmissionAgentAdmin(admin.ModelAdmin):
    inlines = [UnitGreenhouseGasByAgentEmissionInline]
    pass


