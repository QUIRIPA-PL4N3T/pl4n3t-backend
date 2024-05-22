from django.utils.text import slugify
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import QuantificationType, GHGScope, ISOCategory, EmissionSourceGroup, CommonEquipment, CommonActivity, \
    CommonProduct, Investment
from .serializers import (
    QuantificationTypeSerializer,
    GHGScopeSerializer,
    ISOCategorySerializer,
    EmissionSourceGroupSerializer, CommonEquipmentSerializer, CommonActivitySerializer, CommonProductSerializer,
    InvestmentSerializer
)
from django.utils.translation import gettext_lazy as _


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
    serializer_class = EmissionSourceGroupSerializer
    permission_classes = [permissions.AllowAny]


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


@extend_schema(tags=['EmissionSourceGroups'])
class CommonEquipmentViewSet(BaseSearchViewSet):
    queryset = CommonEquipment.objects.all()
    serializer_class = CommonEquipmentSerializer


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
