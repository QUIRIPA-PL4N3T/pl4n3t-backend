from django.contrib import admin
from accounts.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Definir los campos a mostrar en el admin
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_editable = ('is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Company Info'), {'fields': ('company',)}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ('-email',)
