from django.contrib import admin
from emission_source_classifications.models import ISOCategory, GHGScope, EmissionSourceGroup, QuantificationType


@admin.register(QuantificationType)
class QuantificationTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description']


@admin.register(ISOCategory)
class ISOCategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description']


@admin.register(GHGScope)
class GHGScopeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'description']


@admin.register(EmissionSourceGroup)
class EmissionSourceGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('emission_factor_type',)
