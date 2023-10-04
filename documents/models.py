import os
import sys
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.dispatch import receiver
from django.urls import reverse
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
from main.base import Generic, Base, GenericManager
from main.settings import UPLOAD_TO
from documents.utils import _delete_file, get_file_type
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.sites.models import Site

fs = FileSystemStorage(location=settings.MEDIA_ROOT)


# Create your models here.
def upload_location(instance, filename):
    return f"{UPLOAD_TO}/{instance.content_type.model}/{instance.object_pk}/{filename}"


class Document(Base, Generic):
    file = models.FileField(storage=fs, upload_to=upload_location)
    thumbnails = models.FileField(storage=fs, max_length=300, upload_to=upload_location, blank=True, null=True)
    file_type = models.CharField('Tipo de archivo', max_length=200, blank=True, null=True)
    size = models.BigIntegerField(_('Tamaño'), default=0)
    is_multimedia = models.BooleanField(_('Es un Archivo Multimedia'), default=False)
    title = models.CharField(max_length=200, blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, null=True, help_text=_('Una Lista separada por comas'))

    objects = GenericManager()

    @classmethod
    def create(cls, file, title, user_created, content_type, object_pk):
        instance = cls(
            file=file,
            title=title,
            user_created=user_created,
            content_type=content_type,
            object_pk=object_pk
        )
        instance.save()
        return instance

    def get_tags_list(self):
        if self.tags:
            return [item.lower() for item in self.tags.split(',')]
        return []

    def get_absolute_url(self, thumbnail: bool = False):
        try:
            return "https://%s%s" % (Site.objects.get_current().domain, self.file.url)
        except:
            return self.file.url

    def get_thumbnails_absolute_url(self):
        try:
            return "https://%s%s" % (Site.objects.get_current().domain, self.thumbnails.url)
        except:
            return self.file.url

    @property
    def document_content_type(self):
        return get_file_type(self.file_type)

    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return self.file.name[len(UPLOAD_TO) + 1:]

    def get_download_url(self):
        return reverse('documents_document_download', args=(self.pk,))

    def save(self, **kwargs):
        # Opening the uploaded image
        try:
            kwargs['force_insert'] = True
            # original_image = Image.open(self.file)
            thumbnails_image = Image.open(self.file)

            # original_output = BytesIO()
            thumbnails_output = BytesIO()

            if thumbnails_image.height > 300 or thumbnails_image.width > 300:
                output_size = (300, 169)
                thumbnails_image.thumbnail(output_size)
                thumbnails_image.save(thumbnails_output, format='JPEG', quality=90)
            # TODO: resize image enable
            # Resize/modify the image
            # original_image = original_image.resize((1080, 1920))

            # After modifications, save it to the output
            # original_image.save(original_output, format='JPEG', quality=90)
            # original_output.seek(0)
            unique_id = get_random_string(length=32)

            # change the imagefield value to be the newley modifed image value
            # self.file = InMemoryUploadedFile(
            #     original_output,
            #     'ImageField', "%s.jpg" % self.file.name.split('.')[0],
            #     'image/jpeg',
            #     sys.getsizeof(original_output), None
            # )
            self.thumbnails = InMemoryUploadedFile(
                thumbnails_output,
                'ImageField',
                "%s.jpg" % unique_id,
                'image/jpeg',
                sys.getsizeof(thumbnails_output), None
            )
            super(Document, self).save()
        except:
            super(Document, self).save()

    class Meta:
        ordering = ('-created',)


@receiver(models.signals.post_delete, sender=Document)
def delete_file(sender, instance, *args, **kwargs):
    """ Deletes files on `post_delete` """
    if instance.file:
        _delete_file(instance.file.path)
