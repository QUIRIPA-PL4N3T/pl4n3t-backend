from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import UnitOfMeasure, MEASURE_TYPE_CHOICES, MEASURE_TYPE_UNKNOWN


class GreenhouseGas(models.Model):
    """
    Represents a specific greenhouse gas with details regarding its impact on global warming.

    Attributes:
    - name (str): Full name of the greenhouse gas.
    - acronym (str): Acronym or abbreviation of the greenhouse gas.
    - kg_co2_equivalence (float): Equivalent kilograms of CO₂ that this gas represents.
    - pcg_min (str): Minimum percentage contribution of this gas to global warming.
    - pcg_max (str): Maximum percentage contribution of this gas to global warming.
    - lifespan_in_years (str): Duration the gas remains in the atmosphere before decomposing.

    Note:
    The string representation of the instance will display the name followed by the acronym.
    """
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


class SourceType(models.Model):
    """
    Represents the type of source responsible for emissions.

    This class provides details about the specific type of source
    (e.g., mobile, fixed) that can emit greenhouse gases or other pollutants.

    Attributes:
    - name (str): The name of the emission source type.
    - description (str): A brief description of the emission source type.

    Note:
    The string representation of the instance will display only the name of the source type.
    """
    name = models.CharField(_('Nombre'), max_length=255)
    description = models.CharField(_('Descripción'), max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Tipo de Fuente de Emisión')
        verbose_name_plural = _('Tipos de Fuente de Emisión')

    def __str__(self):
        return self.name


class FactorType(models.Model):
    """
       Represents the type of emission factor.

       This class details specific types of factors that contribute to emissions,
       for instance, specific conditions or processes that modify the rate or kind
       of pollutants emitted by a source.

        This class provides details about the specific factor type of source
        (e.g., gas, oil) that can emit greenhouse gases or other pollutants.

       Attributes:
       - name (str): The name of the emission factor type.
       - description (str): A brief description of the emission factor type.

       Note:
       The string representation of the instance will display only the name of the factor type.
       """
    name = models.CharField(_('Nombre'), max_length=255)
    description = models.CharField(_('Descripción'), max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Tipo de Factor de Emisión')
        verbose_name_plural = _('Tipo de Factores de Emisión')

    def __str__(self):
        return self.name


class EmissionFactor(models.Model):
    """
    Represents an emission factor associated with a particular source and factor type.

    This model defines the emission factor, which quantifies the emissions per unit of activity.
    It is linked to a specific source type (e.g., vehicles) and factor type (e.g., specific conditions
    or processes) that indicate under what circumstances or conditions this emission factor is applicable.

    Attributes:
    - name (str): The name of the emission factor.
    - description (str): A brief description of the emission factor.
    - observations (str): additional information of the emission factor.
    - measure_type (str): The type of measure associated with this emission factor.
    - factor_type (ForeignKey): The type of factor associated with this emission.
    - source_type (ForeignKey): The source responsible for these emissions.
    - unit (ForeignKey): The unit of consumption or activity for which the emission factor applies.
    - valid_from (date): The start date of the emission factor's validity.
    - valid_until (date): The end date of the emission factor's validity.

    Note:
    The string representation of the instance displays the name of the emission factor
    followed by the symbol of its associated unit of measure.
    """
    name = models.CharField(_('Nombre'), max_length=255)
    description = models.CharField(_('Descripción'), max_length=255)
    observations = models.TextField(_('Observaciones'), blank=True, null=True)
    measure_type = models.CharField(
        _("Tipo de Medida"),
        max_length=18,
        choices=MEASURE_TYPE_CHOICES,
        help_text=_("Tipo de medida"),
        default=MEASURE_TYPE_UNKNOWN,
    )

    application_percentage = models.FloatField(
        _('Porcentaje de Aplicación'),
        default=1,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text=_('1 equivale al 100%')
    )

    factor_type = models.ForeignKey(
        FactorType,
        on_delete=models.CASCADE,
        verbose_name=_('Tipo de Factor de Emisión'),
        related_name='emission_factors')

    source_type = models.ForeignKey(
        SourceType,
        on_delete=models.CASCADE,
        verbose_name=_('Tipo de Fuente de Emisión'),
        related_name='emission_factors')

    unit = models.ForeignKey(
        UnitOfMeasure,
        verbose_name=_('Unidad de Consumo'),
        on_delete=models.CASCADE,
        related_name='+')

    valid_from = models.DateField(_('Válido desde'), null=True, blank=True)
    valid_until = models.DateField(_('Válido hasta'), null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Factor de Emisión')
        verbose_name_plural = _('Factores de Emisión')

    def __str__(self):
        return f'{self.name} ({self.unit.symbol})'


class EmissionFactorComponent(models.Model):
    emission_factor = models.ForeignKey(
        EmissionFactor,
        on_delete=models.CASCADE,
        related_name='components',
        verbose_name=_('Factor de Emisión Principal')
    )
    component_factor = models.ForeignKey(
        EmissionFactor,
        on_delete=models.CASCADE,
        related_name='component_of',
        verbose_name=_('Factor de Emisión Componente')
    )
    application_percentage = models.FloatField(
        _('Porcentaje de Aplicación'),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text=_('1 equivale al 100%')
    )
    component_name = models.CharField(_('Nombre del Componente'), max_length=255)

    class Meta:
        verbose_name = _('Componente de Factor de Emisión')
        verbose_name_plural = _('Componentes de Factor de Emisión')

    def __str__(self):
        return f'{self.component_name}: {self.application_percentage}%'


class GreenhouseGasEmission(models.Model):
    """
    Represents an emission of a specific greenhouse gas.

    This model captures the details about the emission of a specific greenhouse gas,
    which is quantified using an emission factor and measured in a specific unit.
    It also includes other details such as the bibliographic source,
    percentage uncertainty, and maximum allowed amount for the emission.

    Attributes:
    - greenhouse_gas (GreenhouseGas): The type of greenhouse gas being emitted.
    - unit (UnitOfMeasure): The measurement unit for the emission factor.
    - emission_factor (EmissionFactor): The emission factor quantifying the emissions per unit of activity.
    - value (float): The actual amount of gas emitted.
    - bibliographic_source (str): A textual reference to the source of information.
    - percentage_uncertainty (float): Uncertainty associated with the emission value.
    - maximum_allowed_amount (float): The maximum permissible quantity for this emission.

    Note:
    The string representation of the instance displays the emission factor,
    the emitted value, and the acronym of the greenhouse gas.
    """
    greenhouse_gas = models.ForeignKey(
        GreenhouseGas,
        verbose_name=_('Gas de efecto invernadero'),
        on_delete=models.CASCADE,
        related_name='greenhouse_gases')

    unit = models.ForeignKey(
        UnitOfMeasure,
        verbose_name=_('Unidad Factor de Emisión'),
        on_delete=models.CASCADE,
        related_name='+')

    emission_factor = models.ForeignKey(
        EmissionFactor,
        on_delete=models.CASCADE,
        related_name='greenhouse_emission_gases')

    value = models.FloatField(
        _('Cantidad de Emisión'), default=0)

    bibliographic_source = models.TextField(
        blank=True,
        null=True
    )

    percentage_uncertainty = models.FloatField(
        _('Porcentaje de Incertidumbre'), default=0)

    maximum_allowed_amount = models.FloatField(
        _('Cantidad Máxima Permitida'), default=0)

    class Meta:
        ordering = ('emission_factor__source_type', 'emission_factor', 'emission_factor__source_type',
                    'greenhouse_gas__name',)
        verbose_name = _('Emisión de Gas de Efecto Invernadero')
        verbose_name_plural = 'Emisiones de Gases de Efecto Invernadero'

    def __str__(self):
        return f'{self.emission_factor} {self.value} {self.greenhouse_gas.acronym}'


class EmissionResult(models.Model):
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

    MONTH_CHOICES = [
        ('1', _('Enero')),
        ('2', _('Febrero')),
        ('3', _('Marzo')),
        ('4', _('Abril')),
        ('5', _('Mayo')),
        ('6', _('Junio')),
        ('7', _('Julio')),
        ('8', _('Agosto')),
        ('9', _('Septiembre')),
        ('10', _('Octubre')),
        ('11', _('Noviembre')),
        ('12', _('Diciembre')),
    ]

    emission_source = models.ForeignKey(
        'companies.EmissionsSource',
        on_delete=models.CASCADE,
        related_name='emission_results',
        blank=True,
        null=True,

    )
    location = models.ForeignKey(
        'companies.Location',
        on_delete=models.CASCADE,
        related_name='emission_results',
        blank=True,
        null=True,

    )

    user_created = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        null=True,
        related_name='emission_results'
    )

    name = models.CharField(_('Nombre'), max_length=255)
    date = models.DateField(_('Fecha'))
    usage = models.FloatField(_('Uso'))
    month = models.CharField(_('Mes'), max_length=9, choices=MONTH_CHOICES, default='1')
    year = models.PositiveSmallIntegerField(_('Año'), default=2024)
    unit = models.ForeignKey(UnitOfMeasure, verbose_name=_('Unidad de Medida'), on_delete=models.CASCADE)
    total_co2e = models.FloatField(_('Total CO₂e'), default=0)

    def calculate_totals(self):
        # Calculate total emissions per gas
        total_emissions_gas = {}
        for detail in self.gas_details.all():
            if detail.greenhouse_gas not in total_emissions_gas:
                total_emissions_gas[detail.greenhouse_gas] = {
                    'value': 0,
                    'co2e': 0
                }
            total_emissions_gas[detail.greenhouse_gas]['value'] += detail.value
            total_emissions_gas[detail.greenhouse_gas]['co2e'] += detail.co2e

        for greenhouse_gas, totals in total_emissions_gas.items():
            TotalEmissionGas.objects.create(
                emission_result=self,
                greenhouse_gas=greenhouse_gas,
                value=totals['value'],
                co2e=totals['co2e']
            )

        # Calculate total CO2e per component
        co2_by_component = {}
        for detail in self.gas_details.all():
            if detail.emission_factor not in co2_by_component:
                co2_by_component[detail.emission_factor] = 0
            co2_by_component[detail.emission_factor] += detail.co2e

        for emission_factor, total_co2e in co2_by_component.items():
            Co2ByComponent.objects.create(
                emission_result=self,
                emission_factor=emission_factor,
                co2e=total_co2e
            )

    class Meta:
        ordering = ('date', 'name')
        verbose_name = _('Resultado de Emisión')
        verbose_name_plural = _('Resultados de Emisión')

    def __str__(self):
        return f'{self.name} ({self.date})'


class EmissionGasDetail(models.Model):
    """
    Represents the detailed emission data for a specific greenhouse gas in a specific emission result.

    Attributes:
    - emission_factor (ForeignKey): The associated emission factor.
    - emission_result (ForeignKey): The associated emission result.
    - greenhouse_gas (ForeignKey): The greenhouse gas being recorded.
    - value (float): The amount of the gas emitted.
    - co2e (float): The CO₂e equivalent for the gas emitted.
    """
    emission_factor = models.ForeignKey(
        EmissionFactor,
        on_delete=models.CASCADE,
        related_name='+',
        blank=True,
        null=True,
        help_text=_('Factor de emisión asociado.')
    )
    emission_result = models.ForeignKey(EmissionResult, related_name='gas_details', on_delete=models.CASCADE)
    greenhouse_gas = models.ForeignKey(GreenhouseGas, verbose_name=_('Gas de Efecto Invernadero'),
                                       on_delete=models.CASCADE)
    value = models.FloatField(_('Cantidad Emitida'), default=0)
    co2e = models.FloatField(_('CO₂e Equivalente'), default=0)

    class Meta:
        ordering = ('emission_result', 'greenhouse_gas')
        verbose_name = _('Detalle de Emisión de Gas por Factor')
        verbose_name_plural = _('Detalles de Emisión de Gases por Factor')

    def __str__(self):
        return f'{self.greenhouse_gas.name} ({self.value})'


class TotalEmissionGas(models.Model):
    """
    Represents the total emission data for a specific greenhouse gas in a specific emission result.

    Attributes:
    - emission_result (ForeignKey): The associated emission result.
    - greenhouse_gas (ForeignKey): The greenhouse gas being recorded.
    - value (float): The amount of the gas emitted.
    - co2e (float): The CO₂e equivalent for the gas emitted.
    """
    emission_result = models.ForeignKey(
        EmissionResult,
        related_name='total_emissions_gas',
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
        ordering = ('emission_result', 'greenhouse_gas')
        verbose_name = _('Detalle de Emisión de Gas')
        verbose_name_plural = _('Detalles de Emisión de Gases')

    def __str__(self):
        return f'{self.greenhouse_gas.name} ({self.value})'


class Co2ByComponent(models.Model):
    """
    Represents the total CO₂e emission data for a specific component factor

    Attributes:
    - emission_result (ForeignKey): The associated emission result.
    - emission_factor (ForeignKey): The associated emission factor.
    - co2e (float): The CO₂e equivalent for the gas emitted.
    """
    emission_result = models.ForeignKey(
        EmissionResult,
        related_name='co2_by_component',
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

    co2e = models.FloatField(_('CO₂e Equivalente'), default=0)

    class Meta:
        ordering = ('emission_result', 'emission_factor')
        verbose_name = _('CO₂e por Componente')
        verbose_name_plural = _('CO₂e por Componentes')

    def __str__(self):
        return f'{self.emission_factor.name} ({self.co2e})'

