from django.contrib import admin
from activities.models import Activity, ActivityGasEmitted, ActivityGasEmittedByFactor


class ActivityGasEmittedInline(admin.TabularInline):
    model = ActivityGasEmitted
    extra = 0


class ActivityGasEmittedByFactorInline(admin.TabularInline):
    model = ActivityGasEmittedByFactor
    fk_name = 'activity'
    extra = 0


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'consumption', 'unit', 'get_total_co2e']
    inlines = [ActivityGasEmittedByFactorInline, ActivityGasEmittedInline]
    search_fields = ['name']
    list_filter = ['date', 'unit']

    def get_total_co2e(self, obj):
        return obj.total_co2e
    get_total_co2e.short_description = 'Total CO₂e'
