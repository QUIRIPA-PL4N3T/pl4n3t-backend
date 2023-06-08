from django.contrib.gis.db import models
from accounts.models import User
from emissions.models import EmissionAgent
from django.utils.translation import gettext_lazy as _
from main.models import City, UnitOfMeasure


class Company(models.Model):
    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    LARGE = 'LARGE'
    SIZE_CHOICES = [
        (SMALL, _('Pequeña (1-50 empleados)')),
        (MEDIUM, _('Mediana (51-200 empleados)')),
        (LARGE, _('Grande (201+ empleados)')),
    ]

    name = models.CharField(_('Nombre'), max_length=255)
    description = models.TextField(_('Descripción'), blank=True, null=True)
    industry = models.CharField(_('Industria'), max_length=255, blank=True, null=True)
    size = models.CharField(_('Tamaño de la Empresa'), max_length=10, choices=SIZE_CHOICES, default=SMALL)
    website = models.CharField(_('Página Web'), max_length=255, blank=True, null=True)
    geo_location = models.PointField(_('Posición geográfica'), null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Compañía')
        verbose_name_plural = _('Compañías')

    def __str__(self):
        return f'{self.name}'


class CompanyUser(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('company', 'user',)
        verbose_name = _('Usuario de Compañía')
        verbose_name_plural = _('Usuarios de las Compañías')

    def __str__(self):
        return f'{self.company.name} - {self.user.first_name} {self.user.last_name}'


class Location(models.Model):
    name = models.CharField(_('Nombre'), max_length=255)
    address = models.TextField(_('Dirección'), )
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='locations')
    country = models.CharField(_('Pais'), max_length=255)
    zip_code = models.CharField(_('Código Postal'), max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='locations')
    geo_location = models.PointField(_('Posición Geográfica'), null=True, blank=True)

    class Meta:
        ordering = ('company__name', 'name')
        verbose_name = _('Sede')
        verbose_name_plural = _('Sedes')

    def __str__(self):
        return f'{self.company.name} - {self.name}'


class LocationEmissionAgent(models.Model):
    name = models.CharField(_('Nombre'), max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='equipments')
    emission_agent = models.ForeignKey(EmissionAgent, on_delete=models.CASCADE, related_name='equipments')
    geo_location = models.PointField(null=True, blank=True)

    class Meta:
        ordering = ('emission_agent__name', 'name')
        verbose_name = _('Agente emisor de una sede')
        verbose_name_plural = _('Agentes emisores por sede')

    def __str__(self):

        return f'{self.location.name}: {self.emission_agent.name}'


class EmissionAgentMonthEntry(models.Model):
    MONTH_CHOICES = [
        ('January', _('Enero')),
        ('February', _('Febrero')),
        ('March', _('Marzo')),
        ('April', _('Abril')),
        ('May', _('Mayo')),
        ('June', _('Junio')),
        ('July', _('Julio')),
        ('August', _('Agosto')),
        ('September', _('Septiembre')),
        ('October', _('Octubre')),
        ('November', _('Noviembre')),
        ('December', _('Diciembre')),
    ]
    register_date = models.DateField()
    emission_agent = models.ForeignKey(LocationEmissionAgent, on_delete=models.CASCADE)
    month = models.CharField(max_length=9, choices=MONTH_CHOICES)
    emission = models.FloatField(default=0.0)
    unit = models.ForeignKey(UnitOfMeasure, on_delete=models.CASCADE, related_name='+')

    class Meta:
        ordering = ('register_date', 'month')
        verbose_name = 'Registro Mensual de Emisión'
        verbose_name_plural = 'Registro Mensual de Emisiones'

    def __str__(self):
        return f'{self.emission_agent} - {self.month}'
