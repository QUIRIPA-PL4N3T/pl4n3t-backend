from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import UnitOfMeasure


class GreenhouseGas(models.Model):
    name = models.CharField(_('Nombre'), max_length=255)
    acronym = models.CharField(_('Sigla'), max_length=255)
    kg_co2_equivalence = models.FloatField(_('Kg de CO₂ Equivalencia'), default=1)
    pcg_min = models.CharField(_('Porcentaje de calentamiento global min'), max_length=255, default=1)
    pcg_max = models.CharField(_('Porcentaje de calentamiento global min'), max_length=255, default=0)
    lifespan_in_years = models.CharField(_('Permanencia en años'), max_length=255)

    class Meta:
        ordering = ('name', 'acronym')
        verbose_name = _('Gas de Efecto Invernadero')
        verbose_name_plural = _('Gases de Efecto Invernadero')

    def __str__(self):
        return f'{self.name} - {self.acronym}'


class EmissionCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Categoría de Emisión')
        verbose_name_plural = _('Categorías de Emisiones')

    def __str__(self):
        return f'{self.name}'


class EmissionFactor(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    unit = models.ForeignKey(UnitOfMeasure, on_delete=models.CASCADE, related_name='+')

    class Meta:
        ordering = ('name',)
        verbose_name = _('Factor de Emisión')
        verbose_name_plural = _('Factores de Emisión')

    def __str__(self):
        return f'{self.name} ({self.unit.symbol})'


class EmissionAgent(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='equipments/', null=True, blank=True)
    category = models.ForeignKey(EmissionCategory, on_delete=models.CASCADE)
    emission_factor = models.ForeignKey(EmissionFactor, on_delete=models.CASCADE)
    factor = models.FloatField(_('Factor de Emisión'), default=0)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Agente Emisor')
        verbose_name_plural = _('Agentes Emisores')

    def __str__(self):
        return f'{self.name}'


class UnitGreenhouseGasByAgentEmission(models.Model):
    greenhouse_gas = models.ForeignKey(GreenhouseGas, on_delete=models.CASCADE, related_name='greenhouse_gases')
    emission_agent = models.ForeignKey(EmissionAgent, on_delete=models.CASCADE, related_name='greenhouse_gases')
    value = models.FloatField(_('Cantidad de Emisión'), default=0)
    maximum_allowed_amount = models.FloatField(_('Cantidad Máxima Permitida'))

    class Meta:
        ordering = ('greenhouse_gas__name',)
        verbose_name = _('Unidad de Emisión de GEI por Agente Emisor')
        verbose_name_plural = 'Unidades de Emisiones de GEI por Agentes emisores'

    def __str__(self):
        return f'{self.emission_agent} {self.value} {self.greenhouse_gas.acronym}'
