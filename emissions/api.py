from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import GreenhouseGas, SourceType, FactorType, EmissionFactor, GreenhouseGasEmission, EmissionGasDetail, \
    EmissionResult
from emissions.serializers import GreenhouseGasSerializer, SourceTypeSerializer, FactorTypeSerializer, \
    EmissionFactorSerializer, \
    GreenhouseGasEmissionSerializer, EmissionFactorListSerializer, EmissionResultSerializer, \
    EmissionResultListSerializer, EmissionResultDetailSerializer
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters


@extend_schema(tags=['GreenhouseGases'])
class GreenhouseGasViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GreenhouseGas.objects.all()
    serializer_class = GreenhouseGasSerializer


@extend_schema(tags=['SourceTypes'])
class SourceTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SourceType.objects.all()
    serializer_class = SourceTypeSerializer


@extend_schema(tags=['FactorTypes'])
class FactorTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FactorType.objects.all()
    serializer_class = FactorTypeSerializer


@extend_schema(tags=['EmissionFactors'])
class EmissionFactorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmissionFactor.objects.all()
    serializer_class = EmissionFactorSerializer

    @extend_schema(
        summary=_("Lista todos las plantillas de la compañía"),
        responses={200: EmissionFactorListSerializer}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = EmissionFactorListSerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=['GreenhouseGasEmissions'])
class GreenhouseGasEmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GreenhouseGasEmission.objects.all()
    serializer_class = GreenhouseGasEmissionSerializer


@extend_schema(tags=['EmissionsResults'])
class SaveEmissionDataView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmissionResultSerializer

    @extend_schema(
        description=_("Iniciar sesión con una cuenta de google"),
        request=EmissionResultSerializer,
        methods=["post"],
        responses={
            201: EmissionResultSerializer,
            404: OpenApiResponse(description=_('los datos no son validos')),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = EmissionResultSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmissionsResultFilter(filters.FilterSet):
    location = filters.NumberFilter(field_name='location_id')
    group = filters.NumberFilter(field_name='emission_source__group_id')
    source_type = filters.NumberFilter(field_name='emission_source__source_type_id')
    factor_type = filters.NumberFilter(field_name='emission_source__factor_type_id')
    year = filters.NumberFilter(field_name='year')
    month = filters.NumberFilter(field_name='month')
    usage = filters.CharFilter(field_name='usage', lookup_expr='icontains')
    unit = filters.CharFilter(field_name='unit__symbol', lookup_expr='icontains')

    class Meta:
        model = EmissionResult
        fields = ['location', 'group', 'source_type', 'factor_type', 'year', 'month', 'usage']


@extend_schema(tags=['EmissionsResults'])
class EmissionResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmissionResult.objects.all().select_related(
        'emission_source', 'location', 'unit').prefetch_related('total_emissions_gas')
    serializer_class = EmissionResultDetailSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = EmissionsResultFilter

    @extend_schema(
        summary=_("Lista todos los resultados de emisiones"),
        responses={200: EmissionResultListSerializer}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).prefetch_related('total_emissions_gas')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = EmissionResultListSerializer(queryset, many=True)
        return Response(serializer.data)
