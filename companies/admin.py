from django.contrib import admin
from companies.models import Company, Member, Location, EmissionsSource, EmissionsSourceMonthEntry, Brand
from django.utils.translation import gettext_lazy as _


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('company', 'user', 'email', 'status', 'role')
    list_filter = ('company__name', 'status', 'role')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(EmissionsSource)
class EmissionsSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'emission_source_name', 'location', 'source_type', 'group')
    list_filter = ('source_type', 'group', 'location__company')
    search_fields = ('name', 'code', 'location__name', 'location__company__name')
    ordering = ('name',)
    raw_id_fields = ('emission_factor', 'emission_factor_unit')

    fieldsets = (
        (_('Información General'), {
            'fields': ('name', 'code', 'description', 'location', 'image', 'group', 'source_type', 'factor_type',
                       'emission_factor', 'emission_factor_unit', 'geo_location')
        }),
        (_('Vehículos'), {
            'fields': ('vehicle_type', 'vehicle_load', 'vehicle_fuel', 'vehicle_capacity', 'vehicle_efficiency',
                       'vehicle_efficiency_unit'),
            'classes': ('collapse',)
        }),
        (_('Electricidad'), {
            'fields': ('electricity_supplier', 'electricity_source', 'electricity_efficiency',
                       'electricity_efficiency_unit', 'know_type_electricity_generation_source'),
            'classes': ('collapse',)
        }),
        (_('Bienes Arrendados'), {
            'fields': ('leased_assets_type', 'leased_assets_durations', 'leased_assets_duration_unit'),
            'classes': ('collapse',)
        }),
        (_('Manejo de Combustible'), {
            'fields': ('fuel_store', 'fuel_management'),
            'classes': ('collapse',)
        }),
        (_('Generación de Vapor'), {
            'fields': ('exist_steam_specific_factor',),
            'classes': ('collapse',)
        }),
        (_('Residuos'), {
            'fields': ('waste_type', 'waste_classification', 'waste_management'),
            'classes': ('collapse',)
        }),
        (_('Inversiones'), {
            'fields': ('investment_type',),
            'classes': ('collapse',)
        }),
        (_('Refrigerantes'), {
            'fields': (
                'refrigerant_capacity', 'refrigerant_capacity_unit', 'has_refrigerant_leaks',
                'has_refrigerant_conversions',
                'final_disposal_of_refrigerants', 'support_actions_refrigerant_equipment'),
            'classes': ('collapse',)
        }),
        (_('Productos'), {
            'fields': ('product_name', 'product_operation_requirements', 'units_sold', 'units_sold_period'),
            'classes': ('collapse',)
        }),
    )

    def emission_source_name(self, obj):
        return obj.emission_source_name

    def group_name(self, obj):
        return obj.group.name if obj.group else ''

    def company_name(self, obj):
        return obj.location.company.name if obj.location and obj.location.company else ''

    emission_source_name.short_description = 'Fuente de Emisión'
    group_name.short_description = 'Grupo'
    company_name.short_description = 'Compañía'


@admin.register(EmissionsSourceMonthEntry)
class EmissionsSourceMonthEntryAdmin(admin.ModelAdmin):
    pass
