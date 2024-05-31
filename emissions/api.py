from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import GreenhouseGas, SourceType, FactorType, EmissionFactor, GreenhouseGasEmission, EmissionGasDetail
from emissions.serializers import GreenhouseGasSerializer, SourceTypeSerializer, FactorTypeSerializer, \
    EmissionFactorSerializer, \
    GreenhouseGasEmissionSerializer, EmissionFactorListSerializer, EmissionResultSerializer
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


@extend_schema(tags=['EmissionsResults'])
class SaveEmissionDataView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmissionResultSerializer

    @extend_schema(
        description=_("Iniciar sesión con una cuenta de google"),
        request=EmissionResultSerializer,
        methods=["post"],
        responses={
            201: OpenApiResponse(description=_('Los datos fuerón guardados con éxito')),
            404: OpenApiResponse(description=_('los datos no son validos')),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = EmissionResultSerializer(data=request.data)
        if serializer.is_valid():
            emission_result = serializer.save()

            # Save each gas detail
            for gas_detail_data in serializer.validated_data['gas_details']:
                EmissionGasDetail.objects.create(
                    emission_result=emission_result,
                    greenhouse_gas=gas_detail_data['greenhouse_gas'],
                    value=gas_detail_data['value'],
                    co2e=gas_detail_data['co2e']
                )

            return Response({"success": "Data saved successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
