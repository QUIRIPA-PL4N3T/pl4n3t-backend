from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from .models import QuantificationType, GHGScope, ISOCategory, EmissionSourceGroup
from .serializers import (
    QuantificationTypeSerializer,
    GHGScopeSerializer,
    ISOCategorySerializer,
    EmissionSourceGroupSerializer
)


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
