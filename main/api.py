import django_filters
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from main.models import Configuration, UnitOfMeasure, EconomicSector, IndustryType, LocationType, State, City, \
    DocumentType, Country, MEASURE_TYPE_CHOICES
from main.serializer import ConfigurationSerializer, UnitOfMeasureSerializer, EconomicSectorSerializer, \
    IndustryTypeSerializer, LocationTypeSerializer, StateSerializer, CitySerializer, DocumentTypeSerializer, \
    CountrySerializer, MeasureTypeSerializer
from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _


@extend_schema(tags=['Main'])
class ConfigurationView(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer


@extend_schema(tags=['Main'])
class CountryViewSet(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateFilter(django_filters.FilterSet):
    country = django_filters.NumberFilter(field_name='country__id')

    class Meta:
        model = State
        fields = ['country']


@extend_schema(tags=['Main'])
class StateViewSet(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = StateFilter


class CityFilter(django_filters.FilterSet):
    state = django_filters.NumberFilter(field_name='state__id')

    class Meta:
        model = City
        fields = ['state']


@extend_schema(tags=['Main'])
class CityViewSet(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CityFilter


@extend_schema(tags=['Main'])
class DocumentTypeViewSet(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer


@extend_schema(tags=['Main'])
class TypeUnitOfMeasureViewSet(GenericAPIView):
    """
    Get:
    Get types of units of measure
    """
    @extend_schema(
        summary=_("Obtiene la información de un usuario mediante el nombre usuario"),
        description=_("Obtiene la información de un usuario mediante el nombre usuario"),
        responses={
            200: MeasureTypeSerializer,
            404: OpenApiResponse(description=_('El Usuario no existe')),
        },
        methods=["get"]
    )
    def get(self, request, *args, **kwargs):
        data = []
        for key, value in MEASURE_TYPE_CHOICES:
            data.append({
                'label': key,
                'value': value,
            })
        return Response(data)


class UnitOfMeasureFilter(filters.FilterSet):
    measure_type = filters.ChoiceFilter(field_name='measure_type', choices=MEASURE_TYPE_CHOICES)
    is_gei_unit = filters.BooleanFilter(field_name='is_gei_unit')

    class Meta:
        model = UnitOfMeasure
        fields = ['measure_type', 'is_gei_unit']


@extend_schema(tags=['Main'])
class UnitOfMeasureViewSet(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer
    filterset_class = UnitOfMeasureFilter

    def get_queryset(self):
        return UnitOfMeasure.objects.filter(is_enabled=True)


@extend_schema(tags=['Main'])
class EconomicSectorViewSet(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = EconomicSector.objects.all()
    serializer_class = EconomicSectorSerializer


@extend_schema(tags=['Main'])
class IndustryTypeViewSet(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = IndustryType.objects.all()
    serializer_class = IndustryTypeSerializer


@extend_schema(tags=['Main'])
class LocationTypeViewSet(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = LocationType.objects.all()
    serializer_class = LocationTypeSerializer
