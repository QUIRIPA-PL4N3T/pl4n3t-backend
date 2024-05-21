import django_filters
from drf_spectacular.utils import extend_schema
from rest_framework.mixins import ListModelMixin
from main.models import Configuration, UnitOfMeasure, EconomicSector, IndustryType, LocationType, State, City, \
    DocumentType, Country
from main.serializer import ConfigurationSerializer, UnitOfMeasureSerializer, EconomicSectorSerializer, \
    IndustryTypeSerializer, LocationTypeSerializer, StateSerializer, CitySerializer, DocumentTypeSerializer, \
    CountrySerializer
from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters


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
class UnitOfMeasureViewSet(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = UnitOfMeasure.objects.all()
    serializer_class = UnitOfMeasureSerializer

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
