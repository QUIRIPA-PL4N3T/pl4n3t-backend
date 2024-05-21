from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from rest_framework.parsers import MultiPartParser, FormParser
from companies.models import Company, Brand, Member, Location, EmissionsSource, EmissionsSourceMonthEntry
from companies.serializers import CompanySerializer, BrandSerializer, MemberSerializer, LocationSerializer, \
    EmissionsSourceSerializer, EmissionsSourceMonthEntrySerializer, CompanyLogoSerializer
from django_filters import rest_framework as filters


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
