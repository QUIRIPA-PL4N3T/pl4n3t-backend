from django.contrib import admin
from main.models import Configuration, UnitOfMeasure


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
