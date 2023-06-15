from django.contrib import admin
from main.models import Configuration, UnitOfMeasure, EconomicSector, IndustryType, LocationType, State, City, \
    DocumentType


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ["key", "value"]


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'symbol', 'measure_type']
    list_editable = ['name', 'symbol', 'measure_type']
    fields = ['name', 'slug', 'symbol', 'measure_type', 'name_standard_unit',
              'scale_to_standard_unit', 'offset_to_standard_unit', 'formula'
              ]
    readonly_fields = ["slug"]
    search_fields = ('name',)
    list_filter = ('measure_type', 'name_standard_unit')


@admin.register(EconomicSector)
class EconomicSectorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(IndustryType)
class IndustryTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(LocationType)
class LocationTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'dane_code', 'geonames_code', 'slug']
    search_fields = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['state', 'name', 'dane_code', 'slug', 'coords_lat', 'coords_long']
    search_fields = ['name']


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name']
