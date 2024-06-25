from django.db.models import Sum, F
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from companies.models import Company, Brand, Member, Location, EmissionsSource, EmissionsSourceMonthEntry
from companies.serializers import CompanySerializer, BrandSerializer, MemberSerializer, LocationSerializer, \
    EmissionsSourceSerializer, EmissionsSourceMonthEntrySerializer, CompanyLogoSerializer, DashboardDataSerializer
from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _
from emissions.models import EmissionGasDetail
from main.contrib.mixins import ListModelMixinWithRequest, CreateModelMixinWithRequest, UpdateModelMixinWithRequest, \
    DestroyModelOwnerMixin, RetrieveModelMixinWithRequest


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
    @action(detail=True, methods=['get'], url_path='members', url_name='members')
    def list_members(self, request, pk=None):
        company = self.get_object()
        members = Member.objects.filter(company=company)
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary='Add a member to a specific company',
        request=MemberSerializer,
        responses={201: MemberSerializer}
    )
    @action(detail=True, methods=['post'], url_path='members', url_name='add_member')
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
class MemberViewSet(viewsets.GenericViewSet, ListModelMixinWithRequest, RetrieveModelMixinWithRequest,
                    CreateModelMixinWithRequest, UpdateModelMixinWithRequest, DestroyModelOwnerMixin):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company_id = self.kwargs.get('company_id')
        print('***********')
        print(company_id)
        print('***********')

        return Member.objects.filter(company_id=company_id)

    @extend_schema(
        summary='List all members of a specific company',
        parameters=[
            OpenApiParameter(
                name='company_id',
                description='ID of the company',
                required=True,
                type=int,
                location=OpenApiParameter.PATH)
        ],
        responses={200: MemberSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='Add a member to a specific company',
        request=MemberSerializer,
        responses={201: MemberSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary='Update a member of a specific company',
        request=MemberSerializer,
        responses={200: MemberSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary='Delete a member from a specific company',
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@extend_schema(tags=['Locations'])
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class EmissionsSourceFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')
    location = filters.NumberFilter(field_name='location_id')
    group = filters.NumberFilter(field_name='group_id')
    source_type = filters.NumberFilter(field_name='source_type_id')
    factor_type = filters.NumberFilter(field_name='factor_type_id')

    class Meta:
        model = EmissionsSource
        fields = ['name', 'code', 'location', 'group', 'source_type', 'factor_type']


@extend_schema(tags=['CompanyEmissionSources'])
class EmissionsSourceViewSet(viewsets.ModelViewSet):
    queryset = EmissionsSource.objects.all()
    serializer_class = EmissionsSourceSerializer
    filterset_class = EmissionsSourceFilter


@extend_schema(tags=['CompanyEmissionSourceEntries'])
class EmissionsSourceMonthEntryViewSet(viewsets.ModelViewSet):
    queryset = EmissionsSourceMonthEntry.objects.all()
    serializer_class = EmissionsSourceMonthEntrySerializer


@extend_schema(tags=['Dashboard'])
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    location = None
    # EmissionResult query by location
    results = None

    def emissions_by_gas(self):
        # Collect data for the summary of emissions by gas
        gas_emissions = EmissionGasDetail.objects.filter(
            emission_result__location_id=self.location.id).values('greenhouse_gas__name').annotate(
            total_value=Sum('value')
        ).order_by('greenhouse_gas__name')
        gas_summary = []

        for gas in gas_emissions:
            percentage_change = self.calculate_percentage_change(gas['greenhouse_gas__name'], self.location.id)
            gas_summary.append({
                'gas_name': gas['greenhouse_gas__name'],
                'total_value': gas['total_value'],
                'percentage_change': percentage_change
            })
        return gas_summary

    def emissions_by_source(self):
        # Collect data for the summary by emission source type
        emission_sources = self.results.values('emission_source__name').annotate(
            value=Sum('total_co2e')
        ).order_by('emission_source__name')
        source_summary = [{'source_type': source['emission_source__name'], 'value': source['value']} for source in
                          emission_sources]
        return source_summary

    def emissions_by_classification_group(self):
        # Collect data for GHG distribution
        gei_distribution = self.results.values('total_co2e').annotate(
            percentage=F('total_co2e') / Sum('total_co2e') * 100
        )
        gei_summary = [{'category': 'GEI', 'percentage': gei['percentage']} for gei in gei_distribution]
        return gei_summary

    def get_total_co2e(self):
        return self.results.aggregate(total=Sum('total_co2e'))['total']

    def calculate_percentage_change(self, gas_name, location_id):
        # Logic to calculate percentage change since last month
        current_month = timezone.now().month
        previous_month = current_month - 1 if current_month > 1 else 12

        current_month_emissions = EmissionGasDetail.objects.filter(
            emission_result__location=self.location.id,
            greenhouse_gas__name=gas_name,
            emission_result__location_id=location_id,
            emission_result__date__month=current_month
        ).aggregate(total=Sum('value'))['total'] or 0

        previous_month_emissions = EmissionGasDetail.objects.filter(
            greenhouse_gas__name=gas_name,
            emission_result__location_id=location_id,
            emission_result__date__month=previous_month
        ).aggregate(total=Sum('value'))['total'] or 0

        if previous_month_emissions == 0:
            return 100  # Return 100% increase if there were no emissions in the previous month

        percentage_change = ((current_month_emissions - previous_month_emissions) / previous_month_emissions) * 100
        return percentage_change

    @extend_schema(
        summary=_('Recuperar los datos del dashboard para una sede especifica'),
        parameters=[
            OpenApiParameter(name='id', type=OpenApiTypes.INT, description='Location ID', required=True),
        ],
        responses={200: DashboardDataSerializer}
    )
    def get(self, request, *args, **kwargs):
        location_id = request.query_params.get('id')
        if location_id:
            self.location = Location.objects.get(id=location_id)
            self.results = self.location.emission_results.all()

            data = {
                'gas_emissions': self.emissions_by_gas(),
                'emission_sources': self.emissions_by_source(),
                'gei_distribution': self.emissions_by_classification_group(),
                'total_emissions': self.get_total_co2e()
            }
            serializer = DashboardDataSerializer(data)
            return Response(serializer.data)
        return Response({'error': 'location_id is required'}, status=400)
