from django.contrib import admin
from django.utils.html import format_html
from emission_source_classifications.models import ISOCategory, GHGScope, EmissionSourceGroup, QuantificationType, \
    CommonActivity, CommonEquipment, Investment, CommonProduct
from django.utils.translation import gettext_lazy as _


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
    list_display = ('id', 'name', 'form_name', 'description', 'allow_inventory', 'enabled', 'icon_tag')
    list_editable = ('name', 'description', 'allow_inventory', 'enabled')
    readonly_fields = ('form_name',)

    def icon_tag(self, obj):
        if obj.icon:
            return format_html('<img src="{}" style="max-width: 30px; max-height: 30px;" />'.format(obj.icon.url))
        return ""

    icon_tag.short_description = _('Ícono')


@admin.register(CommonActivity)
class CommonActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(CommonEquipment)
class CommonEquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'group']
    list_editable = ['group']
    list_filter = ['group']


@admin.register(CommonProduct)
class CommonProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    pass
