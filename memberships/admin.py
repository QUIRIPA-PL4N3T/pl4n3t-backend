from django.contrib import admin
from memberships.models import Membership, CompanyMembership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyMembership)
class CompanyMembershipAdmin(admin.ModelAdmin):
    pass
