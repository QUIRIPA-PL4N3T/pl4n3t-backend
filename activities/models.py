from typing import List
from django.db import models
from django.utils.translation import gettext_lazy as _
from emissions.models import EmissionFactor, GreenhouseGas
from emissions.utils import calculate_emission, EmissionCalculation
from main.models import UnitOfMeasure


class Activity(models.Model):
    """
    Represents the result of an emission calculation for a specific usage.

    Attributes:
    - emission_source (ForeignKey): The source of the emissions.
    - location (ForeignKey): The location where the emission was recorded.
    - user_created (ForeignKey): The user who created this emission result.
    - name (str): The name of the emission result.
    - date (date): The date of the emission calculation.
    - usage (float): The usage amount for the calculation.
    - month (str): The month of the emission calculation.
    - year (int): The year of the emission calculation.
    - unit (ForeignKey): The unit of measurement for the usage.
    - total_co2e (float): The total CO₂e equivalent for the usage.
    """

    results_by_component = []

    MONTH_CHOICES = [
        (1, _('Enero')),
        (2, _('Febrero')),
        (3, _('Marzo')),
        (4, _('Abril')),
        (5, _('Mayo')),
        (6, _('Junio')),
        (7, _('Julio')),
        (8, _('Agosto')),
        (9, _('Septiembre')),
        (10, _('Octubre')),
        (11, _('Noviembre')),
        (12, _('Diciembre')),
    ]

    emission_source = models.ForeignKey(
        'companies.EmissionsSource',
        on_delete=models.CASCADE,
        related_name='activities',
        blank=True,
        null=True,

    )
    location = models.ForeignKey(
        'companies.Location',
        on_delete=models.CASCADE,
        related_name='activities',
        blank=True,
        null=True,

    )

    user_created = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        null=True,
        related_name='activities'
    )
    name = models.CharField(_('Nombre'), max_length=255, blank=True, null=True)
    description = models.CharField(_('Descripción de la actividad'), max_length=255, blank=True, null=True)
    consumption = models.FloatField(_('Uso'))
    date = models.DateField(_('Fecha'))
    month = models.PositiveSmallIntegerField(_('Mes'), choices=MONTH_CHOICES, default=1)
    year = models.PositiveSmallIntegerField(_('Año'), default=2024)
    unit = models.ForeignKey(
        UnitOfMeasure,
        related_name='+',
        verbose_name=_('Unidad de Medida'),
        on_delete=models.CASCADE
    )

    total_co2e = models.FloatField(_('Total CO₂e'), default=0)

    def get_total_gas_emitted_value_by_gas(self, gas_id):
        try:
            gas = self.gases_emitted.get(greenhouse_gas__id=gas_id)
            return round(gas.value, 7)
        except ActivityGasEmitted.DoesNotExist:
            return 0

    def calculate_gases_emitted(self) -> List[EmissionCalculation]:
        """
        Calculate emissions for the activity.

        Returns:
        - List[EmissionCalculation]: List of calculations by component.
        """
        main_emission_factor = self.emission_source.emission_factor

        self.results_by_component = []

        main_component_result = calculate_emission(
            name=main_emission_factor.main_component_name,
            factor=main_emission_factor,
            consumption=self.consumption,
            application_percentage=main_emission_factor.application_percentage
        )

        self.results_by_component.append(main_component_result)

        # Calculate emissions for each subcomponent
        for component in main_emission_factor.components.all():
            sub_component_result = calculate_emission(
                name=component.component_name,
                factor=component.component_factor,
                consumption=self.consumption,
                application_percentage=component.application_percentage
            )
            self.results_by_component.append(sub_component_result)

        return self.results_by_component

    def save_gases_emitted(self):
        """
        Save calculated gases emitted details for the activity.
        """
        if not self.results_by_component:
            self.results_by_component = self.calculate_gases_emitted()

        # Clear previous records
        self.gases_emitted.all().delete()
        self.gases_emitted_by_factor.all().delete()

        total_emissions_by_gas = {}
        self.total_co2e = 0

        # Save new records
        for component_data in self.results_by_component:
            emission_factor = component_data['emission_factor']
            for gas_data in component_data['results']:
                greenhouse_gas = GreenhouseGas.objects.get(acronym=gas_data['gas'])

                value = gas_data['value']
                co2e = gas_data['co2e']

                # Save gases emitted by factor and activity
                ActivityGasEmittedByFactor.objects.create(
                    activity=self,
                    emission_factor=emission_factor,
                    greenhouse_gas=greenhouse_gas,
                    value=value,
                    co2e=co2e
                )

                # Track total emissions gas
                if greenhouse_gas not in total_emissions_by_gas:
                    total_emissions_by_gas[greenhouse_gas] = {
                        'value': 0,
                        'co2e': 0
                    }
                total_emissions_by_gas[greenhouse_gas]['value'] += value
                total_emissions_by_gas[greenhouse_gas]['co2e'] += co2e

                self.total_co2e += co2e

        # Save gases emitted by activity
        for greenhouse_gas, totals in total_emissions_by_gas.items():
            ActivityGasEmitted.objects.create(
                activity=self,
                greenhouse_gas=greenhouse_gas,
                value=totals['value'],
                co2e=totals['co2e']
            )

        self.save()

    class Meta:
        ordering = ('date', 'name')
        verbose_name = _('Actividad')
        verbose_name_plural = _('Actividades')

    def __str__(self):
        return f'{self.name} ({self.date})'


class ActivityGasEmitted(models.Model):
    """
    Represents the total emission data for a specific greenhouse gas in a specific Activity.

    Attributes:
    - activity (ForeignKey): The associated activity.
    - greenhouse_gas (ForeignKey): The greenhouse gas being recorded.
    - value (float): The amount of the gas emitted.
    - co2e (float): The CO₂e equivalent for the gas emitted.
    """
    activity = models.ForeignKey(
        Activity,
        related_name='gases_emitted',
        on_delete=models.CASCADE
    )

    greenhouse_gas = models.ForeignKey(
        GreenhouseGas,
        verbose_name=_('Gas de Efecto Invernadero'),
        related_name='+',
        on_delete=models.CASCADE
    )
    value = models.FloatField(_('Cantidad Emitida'), default=0)
    co2e = models.FloatField(_('CO₂e Equivalente'), default=0)

    class Meta:
        ordering = ('activity', 'greenhouse_gas')
        verbose_name = _('Gas Emitido por Actividad')
        verbose_name_plural = _('Gases Emitidos por Actividad')

    def __str__(self):
        return f'{self.greenhouse_gas.name} ({self.value})'


class ActivityGasEmittedByFactor(models.Model):  # noqa
    """
    Represents the detailed emission data by emission factor for a specific greenhouse gas in a specific Activity.

    Attributes:
    - activity (ForeignKey): The associated Activity.
    - emission_factor (ForeignKey): The associated emission factor.
    - greenhouse_gas (ForeignKey): The greenhouse gas being recorded.
    - value (float): The amount of the gas emitted.
    - co2e (float): The CO₂e equivalent for the gas emitted.
    """
    activity = models.ForeignKey(
        Activity,
        related_name='gases_emitted_by_factor',
        on_delete=models.CASCADE
    )

    emission_factor = models.ForeignKey(
        EmissionFactor,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True,
        help_text=_('Factor de emisión asociado.')
    )
    greenhouse_gas = models.ForeignKey(
        GreenhouseGas,
        related_name='+',
        verbose_name=_('Gas de Efecto Invernadero'),
        on_delete=models.CASCADE
    )

    value = models.FloatField(_('Cantidad Emitida'), default=0)
    co2e = models.FloatField(_('CO₂e Equivalente'), default=0)

    class Meta:
        ordering = ('activity', 'emission_factor', 'greenhouse_gas')
        verbose_name = _('Gas Emitido por Actividad y Factor')
        verbose_name_plural = _('Gases Emitidos por Actividad y Factor')

    def __str__(self):
        return f'{self.greenhouse_gas.name} ({self.value})'
