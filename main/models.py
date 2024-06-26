from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from slugify import slugify

MEASURE_TYPE_UNKNOWN = "UNKNOWN"
MEASURE_TYPE_QUANTITY = "QUANTITY"
MEASURE_TYPE_AREA = "AREA"
MEASURE_TYPE_LENGTH = "LENGTH"
MEASURE_TYPE_ANGLE = "ANGLE"
MEASURE_TYPE_TIME = "TIME"
MEASURE_TYPE_VELOCITY = "VELOCITY"
MEASURE_TYPE_VOLUME = "VOLUMEN"
MEASURE_TYPE_SCALE = "SCALE"
MEASURE_TYPE_WEIGHT = "WEIGHT"
MEASURE_TYPE_ENERGY = "ENERGY"
MEASURE_TYPE_MASS = "MASS"
MEASURE_TYPE_TEMPERATURE = "TEMPERATURE"
MEASURE_TYPE_PRESSURE = "TEMPERATURE"
MEASURE_TYPE_POWER = "POWER"
MEASURE_TYPE_FREQUENCY = "FREQUENCY"
MEASURE_TYPE_ENERGY_CONSUMPTION = "ENERGY_CONSUMPTION"
GEI_EMISSION = "GEI_EMISSION"

MEASURE_TYPE_CHOICES = [
    (MEASURE_TYPE_UNKNOWN, _("Desconocido")),
    (MEASURE_TYPE_QUANTITY, _("Cantidad")),
    (MEASURE_TYPE_AREA, _("Area")),
    (MEASURE_TYPE_LENGTH, _("Longitud")),
    (MEASURE_TYPE_ANGLE, _("Ángulo")),
    (MEASURE_TYPE_TIME, _("Tiempo")),
    (MEASURE_TYPE_VELOCITY, _("Velocidad")),
    (MEASURE_TYPE_VOLUME, _("Volumen")),
    (MEASURE_TYPE_SCALE, _("Escala")),
    (MEASURE_TYPE_WEIGHT, _("Peso")),
    (MEASURE_TYPE_ENERGY, _("Energía")),
    (MEASURE_TYPE_MASS, _("Masa")),
    (MEASURE_TYPE_TEMPERATURE, _("Temperatura")),
    (MEASURE_TYPE_PRESSURE, _("Presión")),
    (MEASURE_TYPE_POWER, _("Potencia")),
    (MEASURE_TYPE_FREQUENCY, _("Frecuencia")),
    (MEASURE_TYPE_ENERGY_CONSUMPTION, _("Consumo de energía")),
    (GEI_EMISSION, _('Emisiones de gases de efecto Invernadero'))
]


class Configuration(models.Model):
    key = models.CharField(max_length=200)
    value = models.TextField()
    company = models.ForeignKey(
        'companies.Company',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.key


class Country(models.Model):
    """
    Represents countries.
    """
    name = models.CharField(_("Nombre de País"), max_length=255)
    iso_code = models.CharField(_("ISO Code"), max_length=3, unique=True)  # ISO 3166-1 alpha-3 code
    slug = AutoSlugField(populate_from='name')

    class Meta:
        verbose_name = _("País")
        verbose_name_plural = _("Paises")
        ordering = ("name",)

    def __str__(self):
        return self.name


class State(models.Model):
    """
    Departamentos de Colombia
    """
    country = models.ForeignKey(
        Country, related_name="states",
        null=True,
        on_delete=models.CASCADE,
    )
    name = models.CharField(_("Nombre del Departamento"), max_length=255)
    dane_code = models.CharField(_("Código DANE"), max_length=3)
    geonames_code = models.CharField(_("Código GeoNames"), max_length=10, null=True, blank=True)
    slug = AutoSlugField(populate_from='name')

    @classmethod
    def get_state_by_name(cls, name):
        try:
            return cls.objects.get(name__iexact=name)
        except cls.DoesNotExist:
            print(name)
            return None

    class Meta:
        verbose_name = _("Departamento")
        verbose_name_plural = _("Departamentos")
        ordering = ("name",)

    def __str__(self):
        return self.name


class City(models.Model):
    """
    Ciudades de Colombia
    """
    state = models.ForeignKey(
        State,
        related_name='cities',
        verbose_name=_("Municipios"),
        on_delete=models.CASCADE)
    name = models.CharField(_("Nombre del Municipio"), max_length=255)
    dane_code = models.CharField(_("Código DANE"), max_length=3)
    slug = AutoSlugField(populate_from='name')
    coords_lat = models.FloatField(null=True, blank=True)
    coords_long = models.FloatField(null=True, blank=True)
    geo_location = models.PointField(null=True, blank=True)

    @classmethod
    def get_city_by_name(cls, name, state):
        try:
            if state:
                return cls.objects.get(name__iexact=name, state_id=state.id)
            return cls.objects.get(name__iexact=name)
        except cls.DoesNotExist:
            return None

    class Meta:
        verbose_name = _("Municipios")
        verbose_name_plural = _("Municipios")
        ordering = ("name",)

    def __str__(self):
        return '%s, %s' % (self.name, self.state.name)

    def save(self, *args, **kwargs):
        if self.coords_lat:
            point = Point(self.coords_long, self.coords_lat)
            self.location = point
        super(City, self).save(*args, **kwargs)


class DocumentType(models.Model):
    name = models.CharField(_('Tipo de Documento'), max_length=64)
    code = models.CharField(_('Código'), max_length=8)

    class Meta:
        verbose_name = _("Tipo de documento")
        verbose_name_plural = _("Tipos de documento")

    def __str__(self):
        return f"{self.name}"


class UnitOfMeasure(models.Model):
    """Unit Of Measure
    Definition
        Any of the systems devised to measure some physical quantity such distance or area or a system devised
        to measure such things as the passage of time.
        The classes of UnitOfMeasure are determined by the member "measureType." Subclasses are not needed for
        implementation, but their use makes type constraints on measure valued attributes easier to specify.
        -- conversionToISOstandardUnit is not null only if the conversion is a simple scale
    """  # noqa

    name = models.CharField(
        _("Nombre"),
        max_length=256,
        blank=True,
        help_text=_("El(los) nombre(s) de una unidad de medida (udm) particular. Los ejemplos incluirían lo siguiente:"
                    "1) para el área udm - metros cuadrados <br />"
                    "2) para udm Time - segundos <br />"
                    "3) para el área udm - metros <br />"
                    "4) Ángulo udm - grados.",
                    ),
    )
    slug = models.CharField(_("Slug"), max_length=32, blank=True, db_index=True)
    symbol = models.CharField(
        _("Símbolo"),
        max_length=32,
        help_text=_(
            """El símbolo utilizado para esta unidad de medida, como "ft" para pies o "m" para metro.""",
        ),
    )
    measure_type = models.CharField(
        _("Tipo de Medida"),
        max_length=18,
        choices=MEASURE_TYPE_CHOICES,
        help_text=_("Tipo de medida"),
    )
    name_standard_unit = models.CharField(
        _("Nombre de la unidad Estándar"),
        max_length=64,
        blank=True,
        help_text=_(
            "Nombre de las unidades estándar a las que se puede convertir directamente esta unidad de medida"
            "Si esta variable es NULL, entonces la unidad estándar para este tipo de medida dada por el local"
            "copia de la lista de códigos StandardsUnits.",
        ),
    )
    scale_to_standard_unit = models.FloatField(
        _("Escala para la unidad Estándar"),
        blank=True,
        null=True,
        help_text=_(
            "Si el sistema de implementación utilizado para este objeto no es compatible con NULL, la escala se "
            "establece en 0 es equivalente a NULL tanto para la escala como para el desplazamiento.<br />"
            "Si X es la unidad actual y S es la estándar, la escala de dos variables (ToStandardUnit)"
            "y offset(ToStandardUnit) se puede usar para hacer la conversión de X a S por:<br />"
            "S = compensación + escala*X <br />"
            "y, por el contrario, <br />"
            "X = (desplazamiento S)/escala",
        ),
    )
    offset_to_standard_unit = models.FloatField(
        _("Compensación a la unidad estándar"),
        blank=True,
        null=True,
        help_text=_(
            "Consulte scaleToStandardUnit para obtener una descripción. Nuevamente, esta variable es NULL y no es una "
            "conversión lineal es posible. Si las dos unidades son solo una escala en diferencia, entonces este número "
            "es cero (0). Si el sistema de implementación utilizado para este objeto no es compatible con NULL, "
            "entonces el conjunto de escalado a 0 es equivalente a NULL tanto para la escala como para el "
            "desplazamiento",
        ),
    )
    formula = models.CharField(
        _("Formula"),
        blank=True,
        max_length=32,
        help_text=_(
            "Una fórmula algebraica (probablemente en algún lenguaje de programación) que convierte esta unidad de "
            "medida (representada en la fórmula por su uomSymbol) a la norma ISO (representada por su símbolo. "
            "Este atributo de miembro no es obligatorio, pero es una pieza valiosa de documentación",
        ),
    )
    is_enabled = models.BooleanField(_('Activa'), default=False)
    is_gei_unit = models.BooleanField(_('Es una unidad de medida GEI'), default=False)

    def convert_to(self, value, target_unit):
        if not self.scale_to_standard_unit or not target_unit.scale_to_standard_unit:
            raise ValueError("Conversion requires scale to standard unit for both units.")

        # Convert the value to the standard unit
        standard_value = (value + self.offset_to_standard_unit) * self.scale_to_standard_unit

        # Convert the standard value to the target unit
        target_value = (standard_value - target_unit.offset_to_standard_unit) / target_unit.scale_to_standard_unit

        return target_value

    class Meta:
        verbose_name = _("Unidad de Medida")
        verbose_name_plural = _("Unidades de Medida")
        ordering = ["measure_type", "name"]

    def __str__(self):
        return "%s %s" % (self.symbol, self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:32]
        return super().save(*args, **kwargs)


class EconomicSector(models.Model):
    name = models.CharField(_('Nombre del Sector'), max_length=255, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Sector Económico')
        verbose_name_plural = _('Sectores Económicos')

    def __str__(self):
        return self.name


class IndustryType(models.Model):
    name = models.CharField(_('Tipo de Industria'), max_length=255, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Tipo de Industria')
        verbose_name_plural = _('Tipos de Industria')

    def __str__(self):
        return self.name


class LocationType(models.Model):
    name = models.CharField(_('Tipo de sede'), max_length=255, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Tipo de sede')
        verbose_name_plural = _('Tipos de sede')

    def __str__(self):
        return self.name


class WebinarRegistrant(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    company_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.email
