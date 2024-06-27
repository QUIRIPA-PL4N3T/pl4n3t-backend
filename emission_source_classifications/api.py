from django.utils.text import slugify
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from companies.models import EmissionsSource
from emissions.utils import calculate_emission
from .models import QuantificationType, GHGScope, ISOCategory, EmissionSourceGroup, CommonEquipment, CommonActivity, \
    CommonProduct, Investment
from .serializers import (
    QuantificationTypeSerializer,
    GHGScopeSerializer,
    ISOCategorySerializer,
    EmissionSourceGroupListSerializer, EmissionSourceGroupDetailSerializer, CommonEquipmentSerializer, \
    CommonActivitySerializer, CommonProductSerializer,
    InvestmentSerializer, EmissionCalculationResultSerializer, EmissionCalculationInputSerializer
)
from emissions.serializers import FactorTypeSerializer
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters


@extend_schema(tags=['QuantificationTypes'])
class QuantificationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuantificationType.objects.all()
    serializer_class = QuantificationTypeSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=['GHGScopes'])
class GHGScopeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GHGScope.objects.all()
    serializer_class = GHGScopeSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=['ISOCategories'])
class ISOCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ISOCategory.objects.all()
    serializer_class = ISOCategorySerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=['EmissionSourceGroups'])
class EmissionSourceGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EmissionSourceGroup.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = EmissionSourceGroupDetailSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return EmissionSourceGroupListSerializer
        return EmissionSourceGroupDetailSerializer


    @extend_schema(
        summary='Retrieve a list of emission source groups',
        responses={200: EmissionSourceGroupListSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @extend_schema(
        description='Retrieve emission factor types associated with an emission source group.',
        responses={200: FactorTypeSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def emission_factor_types(self, request, pk=None):
        emission_source_group = self.get_object()
        emission_factor_types = emission_source_group.emission_factor_types.all()
        serializer = FactorTypeSerializer(emission_factor_types, many=True)
        return Response(serializer.data)


class BaseSearchViewSet(ListModelMixin, viewsets.GenericViewSet, CreateModelMixin):
    """
    Clase base para ViewSets con funcionalidad de búsqueda.
    """
    search_param = 'search'
    search_field = 'normalized_name__icontains'

    @extend_schema(
        summary=_("Buscar por un texto"),
        parameters=[
            OpenApiParameter(
                name="search",
                description=_('texto a buscar'),
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ],
    )
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get(self.search_param, '')
        if query:
            normalized_query = slugify(query).lower()
            filter_kwargs = {self.search_field: normalized_query}
            results = self.get_queryset().filter(**filter_kwargs)
            serializer = self.get_serializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No query parameter provided."}, status=status.HTTP_400_BAD_REQUEST)


class CommonEquipmentFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    group = filters.NumberFilter(field_name='group_id')

    class Meta:
        model = CommonEquipment
        fields = ['group',]


@extend_schema(tags=['EmissionSourceGroups'])
class CommonEquipmentViewSet(BaseSearchViewSet):
    queryset = CommonEquipment.objects.all()
    serializer_class = CommonEquipmentSerializer
    filterset_class = CommonEquipmentFilter


@extend_schema(tags=['EmissionSourceGroups'])
class CommonActivityViewSet(BaseSearchViewSet):
    queryset = CommonActivity.objects.all()
    serializer_class = CommonActivitySerializer


@extend_schema(tags=['EmissionSourceGroups'])
class CommonProductViewSet(BaseSearchViewSet):
    queryset = CommonProduct.objects.all()
    serializer_class = CommonProductSerializer


@extend_schema(tags=['EmissionSourceGroups'])
class InvestmentViewSet(BaseSearchViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer


@extend_schema(tags=['Calculator'])
class EmissionCalculatorView(GenericAPIView):
    # workaround to remove warning: Failed to obtain model through view's queryset due to raised exception
    queryset = EmissionsSource.objects.none()

    @extend_schema(
        summary="Calculate emissions",
        request=EmissionCalculationInputSerializer,
        responses={200: EmissionCalculationResultSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        # Validate input data
        serializer = EmissionCalculationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        emission_source = get_object_or_404(EmissionsSource, id=data['emission_source_id'])
        consumption = data['consumption']
        unit_of_measure_id = data['unit_of_measure_id']

        # Get the main emission factor associated with the emission source
        main_emission_factor = emission_source.emission_factor

        results = []

        # Calculate emissions for the main component
        main_component_result = calculate_emission(
            name=main_emission_factor.main_component_name,
            factor=main_emission_factor,
            consumption=consumption,
            application_percentage=main_emission_factor.application_percentage
        )

        results.append(main_component_result)

        # Calculate emissions for each subcomponent
        for component in main_emission_factor.components.all():
            sub_component_result = calculate_emission(
                name=component.component_name,
                factor=component.component_factor,
                consumption=consumption,
                application_percentage=component.application_percentage
            )
            results.append(sub_component_result)

        # Serialize the results and send the response
        result_serializer = EmissionCalculationResultSerializer(results, many=True)
        return Response(result_serializer.data, status=status.HTTP_200_OK)
