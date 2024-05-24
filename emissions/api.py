from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from reports.serializers import CompanyTemplateListSerializer
from .models import GreenhouseGas, SourceType, FactorType, EmissionFactor, GreenhouseGasEmission
from emissions.serializers import GreenhouseGasSerializer, SourceTypeSerializer, FactorTypeSerializer, \
    EmissionFactorSerializer, \
    GreenhouseGasEmissionSerializer, EmissionFactorListSerializer
from django.utils.translation import gettext_lazy as _


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
