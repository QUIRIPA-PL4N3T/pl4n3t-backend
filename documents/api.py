from django.contrib.contenttypes.models import ContentType
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from documents.models import Document
from documents.serializer import DocumentSerializer
from main.settings import get_platform_object_types
from main.contrib.mixins import UpdateModelMixinWithRequest, DestroyModelOwnerMixin, UserCreateMixinViewSet
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.settings import api_settings
from django.utils.translation import gettext_lazy as _


class DocumentViewSet(viewsets.GenericViewSet, UpdateModelMixinWithRequest, DestroyModelOwnerMixin,
                      UserCreateMixinViewSet):
    serializer_class = DocumentSerializer
    parser_classes = (
        parsers.MultiPartParser,
        parsers.FormParser,
        parsers.JSONParser,
    )
    queryset = Document.objects.none()
    # Settings with different objects types that allow set documents
    object_types = get_platform_object_types()

    def get_queryset(self):
        return self.get_user_queryset(Document)

    def get_object_by_name_and_id(self, model_name, model_id):
        try:
            model = self.object_types[model_name]
            return model.objects.get(id=model_id)
        except KeyError:
            return None
        except ObjectDoesNotExist:
            return None

    def create_document(self, request, model):
        content_type = ContentType.objects.get_for_model(model)
        # add additional fields
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(content_type=content_type, object_pk=model.pk, user_created=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    @extend_schema(
        summary=_("Anexar documento a un modelo de datos"),
        description=f'Anexa un documento a un modelo de datos: {", ".join(item for item in object_types)}',
        parameters=[
            OpenApiParameter(
                name="object_type",
                description=f'Tipo de objeto a que al que se va anexar el documento: {", ".join(item for item in object_types)}',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH),
            OpenApiParameter(
                name="object_pk",
                description='Id del objeto al que se va anexar el documento',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH),  # path variable was overridden
        ],
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'file': {'type': 'string', 'format': 'binary'},
                    'title': {"type": "string"},
                    'tags': {"type": "string"},
                }
            }
        },
        # request=DocumentSerializer,
        responses={200: DocumentSerializer},
        methods=["post"]
    )
    @action(
        methods=['post'],
        detail=False,
        url_path=r'(?P<object_type>[\w\-]+)/(?P<object_pk>\d+)',
        url_name='document-create'
    )
    def create_document_action(self, request, object_type, object_pk):
        model = self.get_object_by_name_and_id(object_type, object_pk)
        if not model:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return self.create_document(request, model)
