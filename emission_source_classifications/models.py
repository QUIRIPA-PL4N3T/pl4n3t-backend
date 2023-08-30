from django.db import models
from django.utils.translation import gettext_lazy as _
from emissions.models import EmissionFactor, FactorType


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
    description = models.TextField(_('Descripción'), blank=True, null=True)
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

    class Meta:
        ordering = ('name',)
        verbose_name = _('Grupo de fuente de emisión')
        verbose_name_plural = _('Grupos de fuentes de emisión')

    def __str__(self):
        return self.name
