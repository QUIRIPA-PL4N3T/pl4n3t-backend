from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emissions'
    verbose_name = _('Configuración Factores de emisión')
