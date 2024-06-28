from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from documents.serializer import DocumentSerializer
from .models import Activity
from activities.serializers import ActivitySerializer, ActivityListSerializer, ActivityResponseSerializer
from django_filters import rest_framework as filters
from django.contrib.contenttypes.models import ContentType


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
    serializer_class = ActivityResponseSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ActivityFilter
    pagination_class = CustomPagination
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

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

    @extend_schema(
        summary='Create a new activity with documents',
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'documents': {
                        'type': 'array',
                        'items': {
                            'type': 'string',
                            'format': 'binary'
                        }
                    },
                    'emission_source': {'type': 'integer'},
                    'location': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'consumption': {'type': 'number'},
                    'date': {'type': 'string', 'format': 'date'},
                    'month': {'type': 'integer'},
                    'year': {'type': 'integer'},
                    'unit': {'type': 'integer'}
                }
            }
        },
        responses={201: ActivityResponseSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = ActivitySerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        activity = serializer.save()

        headers = self.get_success_headers(serializer.data)
        response_serializer = ActivityResponseSerializer(activity, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ActivityResponseSerializer(instance, context={'request': request})
        return Response(serializer.data)
