from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from .models import GreenhouseGas, SourceType, FactorType, EmissionFactor, GreenhouseGasEmission
from emissions.serializers import GreenhouseGasSerializer, SourceTypeSerializer, FactorTypeSerializer, EmissionFactorSerializer, \
    GreenhouseGasEmissionSerializer


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


@extend_schema(tags=['GreenhouseGasEmissions'])
class GreenhouseGasEmissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GreenhouseGasEmission.objects.all()
    serializer_class = GreenhouseGasEmissionSerializer
