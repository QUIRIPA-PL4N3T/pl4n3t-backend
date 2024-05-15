from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _


class Membership(models.Model):
    FREE = 'FREE'
    BASIC = 'BASIC'
    PREMIUM = 'PREMIUM'
    ELITE = 'ELITE'

    MEMBERSHIP_CHOICES = [
        (FREE, _('Gratuito')),
        (BASIC, _('Básica')),
        (PREMIUM, _('Premium')),
        (ELITE, _('Elite')),
    ]
    name = models.CharField(_('Nombre'), max_length=255)

    membership_type = models.CharField(
        _('Tipo de Membresía'),
        max_length=50,
        choices=MEMBERSHIP_CHOICES,
        default=FREE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(_('Duración en días'), default=365)
    description = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    num_brands = models.IntegerField(_('Número de Marcas'), default=1)
    num_locations = models.IntegerField(_('Número de Sedes'), default=1)
    num_users = models.IntegerField(_('Usuarios por organización'), default=1)
    emission_sources = models.BooleanField(_('Registro de todas las Fuentes de emisión'), default=True)
    footprint_types = models.CharField(_('Tipos de huella'), max_length=255, default='Huella de Carbono')
    liquidation_options = models.CharField(
        _('Liquidación: Mensual, Trimestral, Anual'),
        max_length=255,
        default='Anual'
    )
    analysis_tools = models.BooleanField(
        _('Herramientas de análisis y generación de informes personalizados'),
        default=False
    )
    basic_support = models.BooleanField(
        _('Acceso al soporte básico a través de preguntas frecuentes o correo electrónico'),
        default=True
    )
    storage_capacity = models.CharField(
        _('Mayor capacidad de almacenamiento para archivos y datos'),
        max_length=255,
        default='No sube soportes'
    )
    tutorials = models.BooleanField(
        _('Tutoriales'),
        default=True
    )
    webinars = models.BooleanField(
        _('Webinars, documentación especializada, etc.'),
        default=False
    )
    general_support = models.BooleanField(
        _('Soporte técnico General'),
        default=True
    )
    dedicated_support = models.BooleanField(
        _('Un representante de soporte asignado exclusivamente a la cuenta'),
        default=False
    )
    custom_api_access = models.BooleanField(
        _('Acceso a una API personalizada para desarrollar integraciones personalizadas'),
        default=False
    )

    def __str__(self):
        return self.name


class CompanyMembership(models.Model):
    PENDING = 'PENDING'
    PAID = 'PAID'
    CANCELED = 'CANCELED'
    EXPIRED = 'EXPIRED'

    MEMBERSHIP_STATUS_CHOICES = [
        (PENDING, _('Pending')),
        (PAID, _('Paid')),
        (CANCELED, _('Canceled')),
        (EXPIRED, _('Expired')),
    ]

    company = models.OneToOneField(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='membership',
        null=True,
        blank=True,
    )
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=MEMBERSHIP_STATUS_CHOICES,
        default=PENDING,
    )

    def __str__(self):
        return f'{self.company.name} - {self.membership.name}'
