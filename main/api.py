import django_filters
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from main.models import Configuration, UnitOfMeasure, EconomicSector, IndustryType, LocationType, State, City, \
    DocumentType, Country, MEASURE_TYPE_CHOICES
from main.serializer import ConfigurationSerializer, UnitOfMeasureSerializer, EconomicSectorSerializer, \
    IndustryTypeSerializer, LocationTypeSerializer, StateSerializer, CitySerializer, DocumentTypeSerializer, \
    CountrySerializer, MeasureTypeSerializer, ConfigurationDetailSerializer, UnitConversionSerializer
from rest_framework import viewsets, permissions, status
from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _


@extend_schema(tags=['Main'])
class ConfigurationView(viewsets.GenericViewSet, ListModelMixin):
    permission_classes = [permissions.AllowAny]
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer


class ConfigurationFilter(django_filters.FilterSet):
    company = django_filters.NumberFilter(field_name='company', lookup_expr='exact')

    class Meta:
        model = Configuration
        fields = ['company']


@extend_schema(tags=['Main'])
class ConfigurationDetailView(viewsets.GenericViewSet, RetrieveModelMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = ConfigurationDetailSerializer
    queryset = Configuration.objects.all()
    filterset_class = ConfigurationFilter
    lookup_field = 'key'

    def get_queryset(self):
        queryset = Configuration.objects.all()
        filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
        filterset = ConfigurationFilter(self.request.GET, queryset=queryset)
        return filterset.qs

    @extend_schema(
        parameters=[
            OpenApiParameter(name='company', description=_('ID de la compañía'), required=False, type=int),
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


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
        summary=_("Obtiene una lista con los tipos de unidades de medida"),
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

    @action(
        detail=False,
        methods=['post'],
        url_path='convert',
        serializer_class=UnitConversionSerializer
    )
    def convert(self, request):
        serializer = UnitConversionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from_unit = serializer.validated_data['from_unit']
        to_unit = serializer.validated_data['to_unit']
        value = serializer.validated_data['value']

        try:
            converted_value = from_unit.convert_to(value, to_unit)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'converted_value': converted_value}, status=status.HTTP_200_OK)

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
