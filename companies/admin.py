from django.contrib import admin
from companies.models import Company, CompanyUser, Location, EmissionsSource, EmissionsSourceMonthEntry, Brand


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(EmissionsSource)
class EmissionsSourceAdmin(admin.ModelAdmin):
    pass


@admin.register(EmissionsSourceMonthEntry)
class EmissionsSourceMonthEntryAdmin(admin.ModelAdmin):
    pass
