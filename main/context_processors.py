from django.conf import settings


def pl4n3t(request):
    return {
        'PL4N3T_APPLICATION': settings.PL4N3T_APPLICATION
    }
