from django.contrib import admin
from companies.models import Company, CompanyUser, Location, LocationEmissionAgent, EmissionAgentMonthEntry


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(LocationEmissionAgent)
class LocationEmissionAgentAdmin(admin.ModelAdmin):
    pass


@admin.register(EmissionAgentMonthEntry)
class EmissionAgentMonthEntryAdmin(admin.ModelAdmin):
    pass
