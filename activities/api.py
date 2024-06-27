from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Activity
from activities.serializers import ActivitySerializer, ActivityListSerializer
from django_filters import rest_framework as filters


class CustomPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


class ActivityFilter(filters.FilterSet):
    location = filters.NumberFilter(field_name='location_id')
    group = filters.NumberFilter(field_name='emission_source__group_id')
    source_type = filters.NumberFilter(field_name='emission_source__source_type_id')
    factor_type = filters.NumberFilter(field_name='emission_source__factor_type_id')
    year = filters.NumberFilter(field_name='year')
    month = filters.NumberFilter(field_name='month')
    usage = filters.CharFilter(field_name='usage', lookup_expr='icontains')
    unit = filters.CharFilter(field_name='unit__symbol', lookup_expr='icontains')

    class Meta:
        model = Activity
        fields = ['location', 'group', 'source_type', 'factor_type', 'year', 'month', 'usage']


@extend_schema(tags=['Activities'])
class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ActivityFilter
    pagination_class = CustomPagination

    @extend_schema(
        summary='List all activities',
        responses={200: ActivityListSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ActivityListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
