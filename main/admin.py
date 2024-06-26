from django.contrib import admin
from main.models import Configuration, UnitOfMeasure, EconomicSector, IndustryType, LocationType, State, City, \
    DocumentType, WebinarRegistrant, Country
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.auth import get_user_model


class UsernameSearch:
    """The User object may not be auth.User, so we need to provide
    a mechanism for issuing the equivalent of a .filter(user__username=...)
    search in CommentAdmin.
    """

    def __str__(self):
        return 'user__%s' % get_user_model().USERNAME_FIELD


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ["id", "key", "value"]
    list_editable = ["key", "value"]


@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'symbol', 'slug', 'name_standard_unit', 'scale_to_standard_unit',
                    'offset_to_standard_unit', 'is_enabled', 'is_gei_unit']
    list_editable = ['name', 'symbol', 'is_enabled', 'is_gei_unit', 'name_standard_unit', 'scale_to_standard_unit',
                     'offset_to_standard_unit']
    fields = ['name', 'slug', 'symbol', 'measure_type', 'name_standard_unit',
              'scale_to_standard_unit', 'offset_to_standard_unit', 'formula'
              ]
    readonly_fields = ["slug"]
    search_fields = ('name',)
    list_filter = ('measure_type', 'name_standard_unit', 'is_gei_unit', 'is_enabled')


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


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'iso_code', 'slug']
    search_fields = ['name']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name', 'dane_code', 'geonames_code', 'slug']
    list_filter = ['country']
    search_fields = ['name']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['state', 'name', 'dane_code', 'slug', 'coords_lat', 'coords_long']
    search_fields = ['name']


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name']


class WebinarRegistrantResource(resources.ModelResource):
    class Meta:
        model = WebinarRegistrant


@admin.register(WebinarRegistrant)
class WebinarRegistrantAdmin(ImportExportModelAdmin):
    resource_class = WebinarRegistrantResource
