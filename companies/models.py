import json
from datetime import timedelta
from urllib.parse import urljoin
from django.contrib.gis.db import models
from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from accounts.models import User
from emission_source_classifications.models import EmissionSourceGroup, CommonActivity, CommonEquipment, CommonProduct, \
    create_or_get_common_data
from emissions.models import SourceType, EmissionFactor, FactorType
from django.utils.translation import gettext_lazy as _
from main.models import City, UnitOfMeasure, EconomicSector, IndustryType, LocationType, Country, State
from memberships.models import Membership, CompanyMembership


class Company(models.Model):
    """
    Represents a company or business entity.

    The `Company` model is intended to encapsulate all relevant details about a company.
    This includes basic information such as its name, size, and industry, as well as more specific
    attributes like its geographical location and associations with particular economic sectors
    or industry types.

    Attributes:
    - name (str): The name of the company.
    - description (str): A brief description of the company.
    - industry (str): The primary industry in which the company operates.
    - size (str): An indication of the company's size based on the number of employees.
      Can be small, medium, or large.
    - website (str): The URL of the company's official website.
    - geo_location (PointField): The geographical location of the company's main office
      or headquarters.
    - economic_sector (ForeignKey to EconomicSector): The broader economic sector to which
      the company belongs.
    - industry_type (ForeignKey to IndustryType): The specific type of industry that further
      categorizes the company's operations.

    Note:
    The string representation of the instance displays the name of the company.
    """
    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    LARGE = 'LARGE'
    SIZE_CHOICES = [
        (SMALL, _('Pequeña (1-50 empleados)')),
        (MEDIUM, _('Mediana (51-200 empleados)')),
        (LARGE, _('Grande (201+ empleados)')),
    ]

    logo = models.ImageField(_('Logo'), upload_to='company_logos/', blank=True, null=True)
    name = models.CharField(_('Nombre'), max_length=255)
    nit = models.CharField(_('NIT'), max_length=15, unique=True, blank=True, null=True)
    description = models.TextField(_('Descripción'), blank=True, null=True)
    industry = models.CharField(_('Industria'), max_length=255, blank=True, null=True)
    size = models.CharField(_('Tamaño de la Empresa'), max_length=10, choices=SIZE_CHOICES, default=SMALL)
    website = models.CharField(_('Página Web'), max_length=255, blank=True, null=True)
    address = models.CharField(_('Dirección'), max_length=255, blank=True, null=True)
    email = models.EmailField(_('Correo Electrónico'), max_length=255, blank=True, null=True)
    postal_code = models.CharField(_('Código Postal'), max_length=15, blank=True, null=True)
    phone = models.CharField(_('Teléfono'), max_length=20, blank=True, null=True)
    geo_location = models.PointField(_('Posición geográfica'), null=True, blank=True)
    economic_sector = models.ForeignKey(
        EconomicSector,
        verbose_name=_('Sector Económico'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    industry_type = models.ForeignKey(
        IndustryType,
        verbose_name=_('Tipo de Industria'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    country = models.ForeignKey(
        Country,
        verbose_name=_('País de origen'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    state = models.ForeignKey(
        State,
        verbose_name=_('Departamento/Estado/Provincia'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    city = models.ForeignKey(
        City,
        verbose_name=_('Ciudad'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ciiu_code = models.CharField(_('Código CIIU'), max_length=10, blank=True, null=True)

    @property
    def logo_absolute_url(self) -> str:
        try:
            current_site = Site.objects.get_current()
            domain = current_site.domain
            if domain is not None and self.logo:
                return urljoin(domain, self.logo.url)
            return ''
        except:
            return ''

    class Meta:
        ordering = ('name',)
        verbose_name = _('Compañía')
        verbose_name_plural = _('Compañías')

    def __str__(self):
        return f'{self.name}'


class Brand(models.Model):
    """
    Represents a brand owned by a company.

    The `Brand` model encapsulates details about individual brands that are
    associated with a particular company. This model captures basic attributes
    such as brand name, logo, and a brief description.

    Attributes:
    - company (ForeignKey to Company): The company that owns the brand.
    - name (CharField): The name of the brand.
    - description (TextField): A brief description of the brand.
    - logo (ImageField): An image representing the brand's logo.

    Note:
    The string representation of the instance displays the brand name.
    """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='brands')
    name = models.CharField(_('Nombre de la Marca'), max_length=255)
    description = models.TextField(_('Descripción'), blank=True, null=True)
    logo = models.ImageField(_('Logo'), upload_to='brands/', null=True, blank=True)

    @property
    def logo_absolute_url(self) -> str:
        try:
            current_site = Site.objects.get_current()
            domain = current_site.domain
            if domain is not None and self.logo:
                return urljoin(domain, self.logo.url)
            return ''
        except:
            return ''

    class Meta:
        ordering = ('name',)
        verbose_name = _('Marca')
        verbose_name_plural = _('Marcas')

    def __str__(self):
        return f'{self.name}'


class Member(models.Model):
    """
    Represents an association between a company and a user.

    The `Member` model establishes a link between individual users and the companies
    they are associated with, whether as employees, stakeholders, or in any other capacity.
    This relationship can be particularly useful in applications where user privileges,
    roles, or access rights are determined based on their company affiliation.

    Attributes:
    - company (ForeignKey to Company): The company with which the user is associated.
    - user (ForeignKey to User): The individual user linked to the company.\
    - rol company rol

    Note:
    The string representation of the instance combines the name of the company and the
    full name of the user.
    """
    ADMIN = 'ADMIN'
    MANAGER = 'MANAGER'
    EMPLOYEE = 'EMPLOYEE'

    ROLES = [
        (ADMIN, _('Administrador de empresa')),
        (MANAGER, _('Gerente de sede')),
        (EMPLOYEE, _('Empleado')),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='members_roles')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies_roles')
    role = models.CharField(_('Rol'), choices=ROLES, max_length=20, default=EMPLOYEE)

    class Meta:
        ordering = ('company', 'user',)
        verbose_name = _('Usuario de Compañía')
        verbose_name_plural = _('Usuarios de las Compañías')

    def __str__(self):
        return f'{self.company.name} - {self.user.first_name} {self.user.last_name}'


class Location(models.Model):
    """
    Represents a physical location related to a company.

    The `Location` model captures details about a specific location that's associated
    with a company. This can represent branches, offices, warehouses, or any other
    type of facility that a company might have. Each location is defined by its address,
    geographical point, and type.

    Attributes:
    - name (CharField): The name or identifier for the location.
    - address (TextField): The full address of the location.
    - city (ForeignKey to City): The city where the location is situated.
    - country (CharField): The country of the location.
    - zip_code (CharField): The postal code for the location.
    - company (ForeignKey to Company): The company that the location belongs to.
    - geo_location (PointField): The geographical point representing the location on a map.
    - brand (ForeignKey to Brand): The brand that the location belongs to.
    - location_type (ForeignKey to LocationType): The type of location (e.g., office, warehouse).

    Note:
    The string representation of the instance combines the name of the company
    and the specific name of the location.
    """
    name = models.CharField(_('Nombre'), max_length=255)
    address = models.TextField(_('Dirección'), )
    phone = models.CharField(_('Teléfono'), max_length=20, blank=True, null=True)
    email = models.EmailField(_('Correo Electrónico'), max_length=255, blank=True, null=True)
    country = models.ForeignKey(
        Country,
        verbose_name=_('País'),
        related_name='locations',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    state = models.ForeignKey(
        State,
        verbose_name=_('Departamento/Estado/Provincia'),
        related_name='locations',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    city = models.ForeignKey(
        City,
        verbose_name=_('Ciudad'),
        on_delete=models.SET_NULL,
        related_name='locations',
        null=True,
        blank=True,
    )
    zip_code = models.CharField(_('Código Postal'), max_length=255)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='locations'
    )
    geo_location = models.PointField(_('Posición Geográfica'), null=True, blank=True)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Marca'),
        related_name='locations'
    )
    location_type = models.ForeignKey(
        LocationType,
        verbose_name=_('Tipo de Sede'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    employees = models.IntegerField(_('Empleados'), default=0)

    class Meta:
        ordering = ('company__name', 'name')
        verbose_name = _('Sede')
        verbose_name_plural = _('Sedes')

    def __str__(self):
        return f'{self.company.name} - {self.name}'


class EmissionsSource(models.Model):
    """
    Represents the various sources from which emissions originate.

    The `EmissionsSource` model captures information about specific sources that
    contribute to emissions within a particular location. Each source is identified
    by a unique name and code. Additionally, a source is related to a specific type
    and can be associated with a group.

    Attributes:
    - name (CharField): The name or identifier for the emission source.
    - code (CharField): A unique code assigned to the emission source.
    - description (TextField): An optional detailed description of the emission source.
    - location (ForeignKey to Location): The specific location where the emission source is situated.
    - image (ImageField): An optional image representing the emission source.
    - group (ForeignKey to EmissionSourceGroup): The group to which the emission source belongs.
    - source_type (ForeignKey to SourceType): The specific type of emission source.
    - geo_location (PointField): An optional geographical point representing the source's position on a map.

    Note:
    The string representation of the instance shows the name of the emission source.
    """

    WASTE_CHOICES = [
        ('food', _('Residuos de alimentos')),
        ('gardening', _('Residuos de jardinería')),
        ('kitchen', _('Residuos de cocina')),
        ('animals', _('Residuos de animales')),
        ('other', _('Otro')),
    ]

    name = models.CharField(_('Nombre'), max_length=255, blank=True, null=True)
    code = models.CharField(_('Código'), max_length=255, blank=True, null=True)
    description = models.TextField(_('Descripción'), blank=True, null=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='emission_sources'
    )
    image = models.ImageField(
        _('Imagen'),
        upload_to='emission_sources/',
        null=True,
        blank=True)
    group = models.ForeignKey(
        EmissionSourceGroup,
        on_delete=models.CASCADE,
        blank=True,
        related_name='emission_sources'
    )
    source_type = models.ForeignKey(
        SourceType,
        on_delete=models.CASCADE,
        verbose_name=_('Tipo de Fuente de Emisión'),
        blank=True,
        null=True,
        related_name='emission_sources')

    factor_type = models.ForeignKey(
        FactorType,
        on_delete=models.CASCADE,
        verbose_name=_('Factor de Emisión'),
        related_name='emission_sources'
    )

    emission_factor = models.ForeignKey(
        EmissionFactor,
        on_delete=models.CASCADE,
        verbose_name=_('Factor de Emisión'),
        related_name='emission_sources'
    )

    emission_factor_unit = models.ForeignKey(
        'main.UnitOfMeasure',
        on_delete=models.CASCADE,
        verbose_name=_('Unidad por defecto'),
        related_name='emission_sources',
        blank=True,
        null=True,
    )

    geo_location = models.PointField(null=True, blank=True)

    # Vehicle fields
    vehicle_type = models.CharField(_('Tipo de Vehículo'), max_length=128, blank=True, null=True)
    vehicle_load = models.CharField(_('Tipo de Carga'), max_length=128, blank=True, null=True)
    vehicle_fuel = models.CharField(_('Tipo de Combustible'), max_length=128, blank=True, null=True)
    vehicle_capacity = models.FloatField(_('Capacidad'), default=0)
    vehicle_efficiency = models.FloatField(_('Eficiencia del Vehículo'), default=0)
    vehicle_efficiency_unit = models.CharField(_('Unidad de Medida'), max_length=128, blank=True, null=True)

    # Electricity fields
    electricity_supplier = models.CharField(_('Proveedor de Electricidad'), max_length=256, blank=True, null=True)

    electricity_source = models.CharField(_('Fuente de generación'), max_length=256, blank=True, null=True)
    electricity_efficiency = models.FloatField(_('Eficiencia Energética'), blank=True, null=True)
    electricity_efficiency_unit = models.CharField(_('Unidad Eficiencia Energética'), max_length=256, blank=True,
                                                   null=True)
    know_type_electricity_generation_source = models.BooleanField(
        _('Conoce el tipo de fuente de generación de electricidad'),
        default=False
    )

    # leased assets Fields
    leased_assets_type = models.CharField(_('Tipo de bien arrendado'), max_length=128, blank=True, null=True)
    leased_assets_durations = models.IntegerField(_('Duración del contrato de Arrendamiento'), default=0)
    leased_assets_duration_unit = models.CharField(
        _('Unidad de Medida de la duración'), max_length=128, blank=True, null=True)

    # fuel management
    fuel_store = models.CharField(_('Almacenamiento del Combustible'), max_length=256, blank=True, null=True)
    fuel_management = models.CharField(_('Gestión del Combustible'), max_length=256, blank=True, null=True)

    # Steam Generation
    exist_steam_specific_factor = models.BooleanField(default=False)

    # Common fields
    activity_name = models.CharField(_('Nombre de la Actividad'), max_length=255, blank=True, null=True)
    equipment_name = models.CharField(_('Nombre del Equipo'), max_length=255, blank=True, null=True)
    origin = models.CharField(_('origen'), max_length=255, blank=True, null=True)
    energy_efficiency_value = models.FloatField(
        _('Eficiencia energética del equipo o sistema que usa combustible'), default=0)
    energy_efficiency_unit = models.CharField(_('Unidad de Medida'), max_length=128, blank=True, null=True)
    service_life = models.IntegerField(_('Vida Útil'), default=0)
    service_life_unit = models.CharField(_('Unidad de Medida Vida útil'), max_length=128, blank=True, null=True)

    # goods and services acquired
    good_and_service_acquired_type = models.CharField(_('Tipo de Bien o Servicio Adquirido'),
                                                      max_length=128, blank=True, null=True)
    acquired_service = models.CharField(_('Servicio Adquirido'), max_length=128, blank=True, null=True)
    supplier_name = models.CharField(_('Nombre del Proveedor'), max_length=255, blank=True, null=True)
    ghg_emission_are_recorded = models.BooleanField(_('Se registran y monitorean las emisiones GEI'), default=False)

    # waste
    waste_type = models.CharField(_('Tipo de desperdicio'), choices=WASTE_CHOICES,
                                  max_length=128, blank=True, null=True)
    waste_classification = models.CharField(_('Clase de desperdicio'), max_length=128, blank=True, null=True)
    waste_management = models.TextField(_('Manejo de desperdicio'), blank=True, null=True)

    # Investments
    investment_type = models.CharField(_('Tipo de Inversión'), max_length=128, blank=True, null=True)

    # Refrigerants
    refrigerant_capacity = models.FloatField(_('Capacidad'), default=0)
    refrigerant_capacity_unit = models.CharField(_('Unidad de Medida'), max_length=128, blank=True, null=True)
    has_refrigerant_leaks = models.BooleanField(_('¿Existen Fugas del refrigerante en el equipo?'), default=False)
    has_refrigerant_conversions = models.BooleanField(
        _('¿Se han realizado conversiones a refrigerantes con menor potencial de calentamiento global (PCG)?'),
        default=False
    )
    final_disposal_of_refrigerants = models.CharField(
        _('disposición final de refrigerantes'), max_length=128, blank=True, null=True)
    support_actions_refrigerant_equipment = models.CharField(
        _('acciones realiza para el mantenimiento y reparaciones del equipo'), max_length=128, blank=True, null=True)

    # Products
    product_name = models.CharField(_('Nombre del Producto'), max_length=255, blank=True, null=True)

    @property
    def emission_source_name(self) -> str:
        if self.group.form_name == 'ELECTRICITY':
            return self.electricity_supplier
        if self.group.form_name == 'ORGANIZATION_VEHICLES':
            return f"{self.code}: {self.name}"
        if self.group.form_name == 'SERVICES':
            return self.supplier_name
        else:
            return self.name

    @property
    def group_name(self) -> str:
        return self.group.name

    class Meta:
        ordering = ('name',)
        verbose_name = _('Fuente de Emisión')
        verbose_name_plural = _('Fuentes de Emisión')

    def __str__(self):
        return f'{self.name}'


class EmissionsSourceMonthEntry(models.Model):
    """
    Represents a monthly record of emissions for a specific source.

    The `EmissionsSourceMonthEntry` model provides a means to capture monthly data
    related to specific emission sources. This helps in tracking and analyzing the
    emission patterns over time. Each entry corresponds to a month and is associated
    with a particular emission source.

    Attributes:
    - MONTH_CHOICES (List of Tuples): A list of months for selection.
    - register_date (DateField): The date when the entry was recorded.
    - emission_agent (ForeignKey to EmissionsSource): The specific source of the emission.
    - month (CharField): The month for which the entry is being recorded.
    - emission (FloatField): The quantity of the emission for the given month.
    - unit (ForeignKey to UnitOfMeasure): The unit of measurement for the emission.

    Note:
    The string representation of the instance shows the emission source followed by the month.
    """
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
    emission_agent = models.ForeignKey(EmissionsSource, on_delete=models.CASCADE)
    month = models.CharField(max_length=9, choices=MONTH_CHOICES)
    emission = models.FloatField(default=0.0)
    unit = models.ForeignKey(UnitOfMeasure, on_delete=models.CASCADE, related_name='+')

    class Meta:
        ordering = ('register_date', 'month')
        verbose_name = 'Registro Mensual de Emisión'
        verbose_name_plural = 'Registro Mensual de Emisiones'

    def __str__(self):
        return f'{self.emission_agent} - {self.month}'


@receiver(post_save, sender=Company)
def create_free_membership(sender, instance, created, **kwargs):
    if created:
        try:
            free_membership = Membership.objects.get(is_default=True)
            end_date = None if free_membership.duration == -1 else timezone.now() + timedelta(
                days=free_membership.duration)

            CompanyMembership.objects.create(
                company=instance,
                membership=free_membership,
                start_date=timezone.now(),
                end_date=end_date,
                status=CompanyMembership.PAID
            )
        except Membership.DoesNotExist:
            pass


@receiver(post_save, sender=EmissionsSource)
def create_common_data(sender, instance, created, **kwargs):
    create_or_get_common_data(CommonActivity, 'name', instance.activity_name)
    create_or_get_common_data(CommonEquipment, 'name', instance.equipment_name)
    create_or_get_common_data(CommonProduct, 'name', instance.product_name)
