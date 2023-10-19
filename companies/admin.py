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
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(EmissionsSource)
class EmissionsSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'source_type')
    list_filter = ('source_type', 'group')

    fieldsets = (
        (_('Información General'), {
            'fields': ('name', 'code', 'description', 'location', 'image', 'group', 'source_type', 'geo_location')
        }),
        (_('Vehículos'), {
            'fields': ('vehicle_type', 'vehicle_load', 'vehicle_fuel', 'vehicle_capacity', 'vehicle_efficiency', 'vehicle_efficiency_unit'),
            'classes': ('collapse',)
        }),
        (_('Electricidad'), {
            'fields': ('electricity_supplier', 'electricity_source', 'electricity_efficiency', 'electricity_efficiency_unit'),
            'classes': ('collapse',)
        })
    )


@admin.register(EmissionsSourceMonthEntry)
class EmissionsSourceMonthEntryAdmin(admin.ModelAdmin):
    pass
