import json
from django.db import models, IntegrityError
from django.utils.translation import gettext_lazy as _
from emissions.models import EmissionFactor, FactorType
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class QuantificationType(models.Model):
    """
    Represents a type of quantification used to measure environmental impact.

    The `QuantificationType` model is intended to categorize different methodologies or
    strategies for measuring environmental impacts, such as carbon footprints, water footprints,
    or plastic footprints. Each type can provide an overview of the specific metrics and
    calculations associated with that type of quantification.

    Attributes:
    - name (str): The name of the quantification type.
    - code (str): A short code to uniquely identify the quantification type.
    - description (str): A detailed description explaining the specifics of the type.

    Note:
    The string representation of the instance displays the name of the quantification type.
    """
    name = models.CharField(_('Nombre'), max_length=255)
    code = models.CharField(_('Código'), max_length=5)
    description = models.TextField(_('Descripción'), blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Tipo de Cuantificación')
        verbose_name_plural = _('Tipos de Cuantificación')

    def __str__(self):
        return f'{self.name}'


class GHGScope(models.Model):
    """
    Represents a scope classification for greenhouse gas (GHG) emissions.

    The GHG Scope model is used to categorize emissions based on their origin or other relevant criteria.
    For example, Scope 1 emissions might refer to direct emissions from owned or controlled sources,
    while Scope 2 could represent indirect emissions from the generation of purchased energy.

    Attributes:
    - name (str): The name of the GHG scope.
    - quantification_type (FK to QuantificationType): The type of quantification to which this GHG scope relates.
    - code (str): A short code to identify the GHG scope.
    - description (str): A detailed description explaining the specifics of the scope.

    Note:
    The string representation of the instance displays the name of the GHG scope.
    """
    name = models.CharField(_('Nombre'), max_length=255)
    quantification_type = models.ForeignKey(
        QuantificationType,
        on_delete=models.CASCADE,
        related_name='scopes',
        blank=True,
        null=True,
        verbose_name=_('Tipo de Cuantificación')
    )
    code = models.CharField(_('Código'), max_length=5)
    description = models.TextField(_('Descripción'), blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _('Alcance GHG')
        verbose_name_plural = _('Alcances GHG')

    def __str__(self):
        return f'{self.name}'


class ISOCategory(models.Model):
    """
    Represents an ISO category related to greenhouse gas (GHG) emissions.

    The ISOCategory model is used to classify emissions within the context of GHG scopes based on
    International Organization for Standardization (ISO) guidelines. These categories further refine
    the origin or nature of emissions under a specific scope.

    Attributes:
    - name (str): The name of the ISO category.
    - code (str): A short code uniquely identifying the ISO category within its scope.
    - scope (GHGScope): The GHG scope to which the ISO category belongs.
    - description (str): A detailed description of the ISO category.

    Note:
    The `full_code` property provides a combined identifier using both the scope's code and the category's code.
    The string representation of the instance displays the `full_code` followed by the name of the ISO category.
    """
    name = models.CharField(_('Nombre'), max_length=255)
    code = models.CharField(_('Código'), max_length=5)
    scope = models.ForeignKey(
        GHGScope,
        verbose_name=_('Alcance'),
        related_name='categories',
        on_delete=models.CASCADE
    )
    description = models.TextField(_('Descripción'), blank=True, null=True)

    @property
    def full_code(self):
        """Returns the combined code of the GHG scope and the ISO category."""
        return f'{self.scope.code} - {self.code}'

    class Meta:
        ordering = ('code', 'name',)
        verbose_name = _('Categoría ISO')
        verbose_name_plural = _('Categorías ISO')

    def __str__(self):
        return f'{self.full_code}: {self.name}'


class EmissionSourceGroup(models.Model):
    """
    Represents a group of sources responsible for greenhouse gas (GHG) emissions.

    The `EmissionSourceGroup` model is designed to categorize and group various emission sources
    based on their similarities or shared characteristics. Each group can contain one or more
    emission factors that can be used to estimate emissions from sources within the group.

    Attributes:
    - name (str): The name of the emission source group.
    - description (str): A detailed description providing context about the group.
    - icon (ImageField): An optional image or icon representing the emission source group.
    - emission_factors (M2M relation with EmissionFactor): Emission factors associated with
      the sources within this group.

    Note:
    The string representation of the instance displays the name of the emission source group.
    """
    name = models.CharField(_('Nombre'), max_length=255)
    description = RichTextField(_('Descripción'), blank=True, null=True)
    icon = models.ImageField(_('Ícono'), upload_to='groups', blank=True, null=True)
    category = models.ForeignKey(
        ISOCategory,
        verbose_name=_('Categoría'),
        related_name='groups',
        on_delete=models.CASCADE
    )
    emission_factor_types = models.ManyToManyField(
        FactorType,
        related_name='emission_source_group',
        blank=True
    )

    allow_inventory = models.BooleanField(_('Permitir registro de inventario'), default=False)
    enabled = models.BooleanField(_('¿Grupo de clasificación activo?'), default=True)
    form_name = models.CharField(_('Nombre del Formulario'), max_length=255, blank='True', null=True)

    @property
    def classification(self) -> str:
        return self.category.full_code

    class Meta:
        ordering = ('name',)
        verbose_name = _('Grupo de fuente de emisión')
        verbose_name_plural = _('Grupos de fuentes de emisión')

    def __str__(self):
        return self.name


class CommonModel(models.Model):
    name = models.CharField(
        _('Nombre'),
        max_length=255,
        unique=True
    )
    normalized_name = models.CharField(
        _('Nombre normalizado'),
        max_length=255,
        unique=True,
        editable=False
    )

    def save(self, *args, **kwargs):
        self.normalized_name = slugify(self.name).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class CommonEquipment(CommonModel):

    normalized_name = models.CharField(
        _('Nombre normalizado'),
        max_length=255,
        editable=False
    )

    group = models.ForeignKey(
        EmissionSourceGroup,
        related_name='equipment_types',
        verbose_name=_('Grupo'),
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('Tipo de Maquinaría/Equipo')
        verbose_name_plural = _('Tipos de Maquinarías/Equipos')
        unique_together = (('group', 'normalized_name'),)
        ordering = ('name',)


class CommonActivity(CommonModel):
    class Meta:
        verbose_name = _('Tipo de Actividad')
        verbose_name_plural = _('Tipos de Actividades')
        ordering = ('name',)


class CommonProduct(CommonModel):
    class Meta:
        ordering = ('name',)
        verbose_name = _('Tipo de Producto')
        verbose_name_plural = _('Tipos de Productos')


class Investment(CommonModel):
    class Meta:
        ordering = ('name',)
        verbose_name = _('Tipo de Inversion')
        verbose_name_plural = _('Tipos de Inversiones')


def create_or_get_common_data(model_class, name_field, instance_field, group=None):
    """
    Creates or retrieves instances in the specified model based on the provided names.

    :param model_class: The Django model in which the instances are to be created or retrieved.
    :param name_field: The field in the model where the name will be stored.
    :param instance_field: The field in the instance containing the name or list of names.
    :param group: (Optional) The group to which the instance belongs.
    """

    if not instance_field:
        return

    try:
        names = json.loads(instance_field)
        if not isinstance(names, list):
            names = [instance_field]
    except json.JSONDecodeError:
        names = [instance_field]

    for name in names:
        normalized_name = slugify(name).lower()
        defaults = {name_field: name}
        if group:
            defaults['group'] = group

        try:
            model_class.objects.get_or_create(
                normalized_name=normalized_name,
                defaults=defaults
            )
        except IntegrityError:
            pass
