from drf_spectacular.utils import extend_schema
from rest_framework.mixins import ListModelMixin
from main.models import Configuration, UnitOfMeasure, EconomicSector, IndustryType, LocationType, State, City, \
    DocumentType
from main.serializer import ConfigurationSerializer, UnitOfMeasureSerializer, EconomicSectorSerializer, \
    IndustryTypeSerializer, LocationTypeSerializer, StateSerializer, CitySerializer, DocumentTypeSerializer
from rest_framework import viewsets, permissions


@extend_schema(tags=['Main'])
class ConfigurationView(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer


@extend_schema(tags=['Main'])
class StateViewSet(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = State.objects.all()
    serializer_class = StateSerializer


@extend_schema(tags=['Main'])
class CityViewSet(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = City.objects.all()
    serializer_class = CitySerializer


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
