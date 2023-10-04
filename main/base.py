from datetime import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str
from main.settings import CONTENT_TYPE_LIMITE_CHOICES
from django.db.models import Q
from accounts.models import User
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils.translation import gettext_lazy as _


class PlatformModel(models.Model):
    """ Platform base model

    PlatformModel acts as an abstract base clase from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
      + created (DateTime): Store the date time the object was created.
      + modified (DateTime): Store the last date time the object was modified.
    """

    created = models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created'
    )
    modified = models.DateTimeField(
        'created at',
        auto_now=True,
        help_text='Date time on which the object was last modified'
    )

    class Meta:
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']


class PlatformModelGis(gis_models.Model):
    """ Platform base model

    PlatformModel acts as an abstract base clase from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
      + created (DateTime): Store the date time the object was created.
      + modified (DateTime): Store the last date time the object was modified.
    """
    coords_lat = gis_models.FloatField(
        _('Latitud'),
        null=True,
        blank=True
    )
    coords_long = gis_models.FloatField(
        _('Longitud'),
        null=True,
        blank=True
    )

    location = gis_models.PointField(
        _('Ubicación'),
        null=True,
        blank=True)

    geom = gis_models.MultiPolygonField(
        _('Plano'),
        null=True,
        blank=True,
        dim=3,
        srid=4326)

    poly = gis_models.PolygonField(
        _('poly'),
        null=True,
        blank=True,
        srid=4326)

    created = gis_models.DateTimeField(
        'created at',
        auto_now_add=True,
        help_text='Date time on which the object was created'
    )
    modified = gis_models.DateTimeField(
        'created at',
        auto_now=True,
        help_text='Date time on which the object was last modified'
    )

    class Meta:
        abstract = True
        get_latest_by = 'created'
        ordering = ['-created', '-modified']


class BaseManager(models.Manager):
    """
    Base Manager for Base model
    """
    def __init__(self):
        super(BaseManager, self).__init__()

    def get_queryset(self):
        return super(BaseManager, self).get_queryset().filter(trashed=False)


class Base(models.Model):
    """
    Base parent model for all the models
    """
    timestamp = models.DateTimeField(blank=True, db_index=True, auto_now_add=True, null=True)
    user_created = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s',
        verbose_name=_('Subido por')
    )
    created = models.DateTimeField(verbose_name=_("Created"), auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_("Last Updated"), auto_now=True)
    trashed = models.BooleanField(default=False, db_index=True)

    objects = BaseManager()

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)

    # Override save method.
    def save(self,  *args, **kwargs):
        if not self.timestamp:
            self.timestamp = datetime.now()

        update_timestamp = kwargs.pop('update_timestamp', False)
        if update_timestamp:
            self.timestamp = datetime.now()

        super(Base, self).save(*args, **kwargs)

    # Override delete method.
    def delete(self, **kwargs):
        self._forced_delete = kwargs.pop('forced', False)
        if not self._forced_delete:
            model = self.__class__
            kwargs.update({'trashed': True})
            model.objects.filter(pk=self.id).update(**kwargs)
        else:
            super(Base, self).delete(**kwargs)

    class Meta:
        abstract = True


class GenericManager(BaseManager):
    def for_model(self, model):
        """
        QuerySet for all documents for a particular model (either an instance or
        a class).
        """
        content_type = ContentType.objects.get_for_model(model)
        qs = self.get_queryset().filter(content_type=content_type)
        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_str(model._get_pk_val()))
        return qs


def limit_content_type_choices():
    query = None
    for app_label, model in CONTENT_TYPE_LIMITE_CHOICES:
        if query:
            query = query | Q(app_label=app_label, model=model)
        else:
            query = Q(app_label=app_label, model=model)
    return query


class Generic(models.Model):
    """
    Abstract model for generic content types.
    """
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=limit_content_type_choices,
        verbose_name=_('content type'),
        related_name="content_type_set_for_%(class)s",
        on_delete=models.CASCADE,
        db_index=True
    )

    object_pk = models.CharField(
        _('object ID'),
        db_index=True,
        max_length=64
    )

    content_object = GenericForeignKey(
        ct_field="content_type",
        fk_field="object_pk"
    )

    class Meta:
        abstract = True
