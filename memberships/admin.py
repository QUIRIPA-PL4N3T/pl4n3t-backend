from django.contrib import admin
from memberships.models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    pass
