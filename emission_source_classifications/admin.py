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
    filter_horizontal = ('emission_factor_types',)
    list_display = ('id', 'name', 'description', 'allow_inventory', 'icon_tag')
    list_editable = ('name', 'description', 'allow_inventory')

    def icon_tag(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="max-width: 30px; max-height: 30px;" />'.format(obj.icon.url))
        return ""

    icon_tag.short_description = _('Ícono')
