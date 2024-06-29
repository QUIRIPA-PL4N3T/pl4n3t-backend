from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import models
from activities.api import CustomPagination
from companies.models import Company, Brand, Member, Location, EmissionsSource
from companies.quantification import DataAnalysis
from companies.serializers import CompanySerializer, BrandSerializer, MemberSerializer, LocationSerializer, \
    EmissionsSourceSerializer, CompanyLogoSerializer, DashboardDataSerializer, EmissionsSourceRequestSerializer
from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _
from companies.utils import generate_schema_for_emission_source
from main.contrib.mixins import UpdateModelMixinWithRequest


@extend_schema(tags=['Companies'])
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        user = self.request.user
        company_ids = Member.objects.filter(user=user).values_list('company_id', flat=True)
        return Company.objects.filter(id__in=company_ids)

    def perform_create(self, serializer):
        company = serializer.save()

        Member.objects.create(
            user=self.request.user,
            company=company,
            role=Member.ADMIN
        )
    
    @extend_schema(
        summary='List all brands of a specific company',
        responses={200: BrandSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def brands(self, request, pk=None):
        company = self.get_object()
        brands = Brand.objects.filter(company=company)
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='List all locations of a specific company',
        responses={200: LocationSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def locations(self, request, pk=None):
        company = self.get_object()
        locations = Location.objects.filter(company=company)
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='List all members of a specific company',
        responses={200: MemberSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        company = self.get_object()
        members = Member.objects.filter(company=company)
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Add a member to a specific company',
        request=MemberSerializer,
        responses={201: MemberSerializer}
    )
    @action(detail=True, methods=['post'], url_path='add-member', url_name='add-member')
    def add_member(self, request, pk=None):
        company = self.get_object()

        serializer = MemberSerializer(
            data=request.data,
            context={
                'company': company,
                'request': request
            })
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['Companies'],
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'logo': {'type': 'string', 'format': 'binary'},
            }
        }
    })
class CompanyLogoViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    queryset = Company.objects.all()
    serializer_class = CompanyLogoSerializer
    parser_classes = (MultiPartParser, FormParser)


@extend_schema(
    tags=['Brands'],
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'description': {"type": "string"},
                'name': {"type": "string"},
                'company': {"type": "integer"},
                'logo': {'type': 'string', 'format': 'binary'},
            }
        }
    })
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    parser_classes = (MultiPartParser, FormParser)


@extend_schema(tags=['CompanyMembers'])
class MemberViewSet(viewsets.GenericViewSet, UpdateModelMixinWithRequest, DestroyModelMixin):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        return Member.objects.filter(company_id=company_id)

    @extend_schema(
        summary='Update a member of a specific company',
        request=MemberSerializer,
        responses={200: MemberSerializer},
    )
    def update(self, request, *args, **kwargs):
        company = Company.objects.get(id=self.kwargs.get('company_id'))
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            context={
                'request': request,
                'company': company,

            })
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @extend_schema(
        summary='Delete a member from a specific company',
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        company = Company.objects.get(id=self.kwargs.get('company_id'))
        user = self.request.user
        if company.members_roles.filter(user=user, role=Member.ADMIN).exists():
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(tags=['Locations'])
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class EmissionsSourceFilter(filters.FilterSet):
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')
    location = filters.NumberFilter(field_name='location_id')
    group = filters.NumberFilter(field_name='group_id')
    source_type = filters.NumberFilter(field_name='source_type_id')
    factor_type = filters.NumberFilter(field_name='factor_type_id')
    search = filters.CharFilter(method='filter_search')

    class Meta:
        model = EmissionsSource
        fields = ['search', 'code', 'location', 'group', 'source_type', 'factor_type']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(name__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(supplier_name__icontains=value) |
            models.Q(product_name__icontains=value)
        )


@extend_schema(tags=['CompanyEmissionSources'])
class EmissionsSourceViewSet(viewsets.ModelViewSet):
    queryset = EmissionsSource.objects.all()
    serializer_class = EmissionsSourceSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']
    pagination_class = CustomPagination
    filterset_class = EmissionsSourceFilter

    @extend_schema(
        summary='Create a new emission source with documents',
        request=generate_schema_for_emission_source(),
        responses={201: EmissionsSourceSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = EmissionsSourceRequestSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        activity = serializer.save()

        headers = self.get_success_headers(serializer.data)
        response_serializer = EmissionsSourceSerializer(activity, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(
        summary='Update an activity with documents',
        request=generate_schema_for_emission_source(),
        responses={201: EmissionsSourceSerializer}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = EmissionsSourceRequestSerializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        activity = serializer.save()
        response_serializer = EmissionsSourceSerializer(activity)
        return Response(response_serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = EmissionsSourceSerializer(instance, context={'request': request})
        return Response(serializer.data)


@extend_schema(tags=['Dashboard'])
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary=_('Recuperar los datos del dashboard para una sede especifica'),
        parameters=[
            OpenApiParameter(name='company', type=OpenApiTypes.INT, description=_('Id de la Compañía'), required=True),
            OpenApiParameter(name='location', type=OpenApiTypes.INT, description=_('Id de la sede')),
            OpenApiParameter(name='scope', type=OpenApiTypes.INT, description='Id del Alcance'),
            OpenApiParameter(name='category', type=OpenApiTypes.INT, description='Id del Categoría'),
            OpenApiParameter(name='group', type=OpenApiTypes.INT, description='Id Grupo'),
            OpenApiParameter(name='emission_source', type=OpenApiTypes.INT, description='Fuente de Emissión'),
            OpenApiParameter(name='source_type', type=OpenApiTypes.INT, description='Tipo de Fuente e emisión'),
            OpenApiParameter(name='factor_type', type=OpenApiTypes.INT, description='Tipos de Factores de emisión'),
            OpenApiParameter(name='factor', type=OpenApiTypes.INT, description='Factores de emisión'),
            OpenApiParameter(name='initial_date', type=OpenApiTypes.DATE, description='Fecha Inicial'),
            OpenApiParameter(name='end_date', type=OpenApiTypes.DATE, description='Fecha Final'),
            OpenApiParameter(name='year', type=OpenApiTypes.INT, description='Año'),
            OpenApiParameter(name='month', type=OpenApiTypes.DATE, description='Mes'),

        ],
        responses={200: DashboardDataSerializer}
    )
    def get(self, request, *args, **kwargs):
        data_analysis = DataAnalysis(
            company_id=request.query_params.get('company'),
            location_id=request.query_params.get('location', None),
            category_id=request.query_params.get('category', None),
            scope_id=request.query_params.get('scope', None),
            group_id=request.query_params.get('group', None),
            source_type_id=request.query_params.get('source_type', None),
            emission_source_id=request.query_params.get('emission_source', None),
            factor_type_id=request.query_params.get('factor_type', None),
            factor_id=request.query_params.get('factor', None),
            initial_date=request.query_params.get('initial_date', None),
            end_date=request.query_params.get('end_date', None),
            year=request.query_params.get('year', None),
            month=request.query_params.get('month', None),

        )
        data_analysis.calculate()
        serializer = DashboardDataSerializer(data_analysis.data)
        return Response(serializer.data)

