import os
from django.conf import settings

UPLOAD_TO = settings.DOCUMENTS_UPLOAD_TO

if not os.path.exists(UPLOAD_TO):
    os.makedirs(UPLOAD_TO)
    os.chmod(UPLOAD_TO, 0o700)

CONTENT_TYPE_LIMITE_CHOICES = (
    ('companies', 'emissionssource'), # noqa
)


def get_platform_object_types():
    # OBJECT TYPES (string_path, Model)
    # Is used to obtain the related model through the patch parameter
    # example: /documents/emission-source/1/

    from companies.models import EmissionsSource

    return {
        'emission-source': EmissionsSource,
    }
