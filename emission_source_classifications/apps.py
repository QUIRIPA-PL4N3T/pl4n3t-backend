from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmissionSourceClassificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emission_source_classifications'
    verbose_name = _('Clasificación de fuentes de emisión')
