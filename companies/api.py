from django.db.models import Sum, F
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from companies.models import Company, Brand, Member, Location, EmissionsSource, EmissionsSourceMonthEntry
from companies.serializers import CompanySerializer, BrandSerializer, MemberSerializer, LocationSerializer, \
    EmissionsSourceSerializer, EmissionsSourceMonthEntrySerializer, CompanyLogoSerializer, DashboardDataSerializer
from django_filters import rest_framework as filters
from django.utils.translation import gettext_lazy as _
from emissions.models import EmissionGasDetail


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
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


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

    @extend_schema(
        summary=_('Recuperar los datos del dashboard para una sede especifica'),
        parameters=[
            OpenApiParameter(name='id', type=OpenApiTypes.INT, description='Location ID', required=True),
        ],
        responses={200: DashboardDataSerializer}
    )
    def get(self, request, *args, **kwargs):

        location_id = request.query_params.get('id')
        if not location_id:
            return Response({'error': 'location_id is required'}, status=400)

        self.location = Location.objects.get(id=location_id)

        results = self.location.emission_results.all()

        # Collect data for the summary of emissions by gas
        gas_emissions = EmissionGasDetail.objects.filter(
            emission_result__location_id=self.location.id).values('greenhouse_gas__name').annotate(
            total_value=Sum('value')
        ).order_by('greenhouse_gas__name')
        gas_summary = []

        for gas in gas_emissions:
            percentage_change = self.calculate_percentage_change(gas['greenhouse_gas__name'], location_id)
            gas_summary.append({
                'gas_name': gas['greenhouse_gas__name'],
                'total_value': gas['total_value'],
                'percentage_change': percentage_change
            })

        # Collect data for the summary by emission source type
        emission_sources = results.values('emission_source__name').annotate(
            value=Sum('total_co2e')
        ).order_by('emission_source__name')
        source_summary = [{'source_type': source['emission_source__name'], 'value': source['value']} for source in emission_sources]

        # Collect data for GHG distribution
        gei_distribution = results.values('total_co2e').annotate(
            percentage=F('total_co2e') / Sum('total_co2e') * 100
        )
        gei_summary = [{'category': 'GEI', 'percentage': gei['percentage']} for gei in gei_distribution]

        total_emissions = results.aggregate(total=Sum('total_co2e'))['total']

        data = {
            'gas_emissions': gas_summary,
            'emission_sources': source_summary,
            'gei_distribution': gei_summary,
            'total_emissions': total_emissions
        }
        serializer = DashboardDataSerializer(data)
        return Response(serializer.data)

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
