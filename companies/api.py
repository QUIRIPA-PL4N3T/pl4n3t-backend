from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from companies.models import Company, Brand, Member, Location, EmissionsSource, EmissionsSourceMonthEntry
from companies.serializers import CompanySerializer, BrandSerializer, MemberSerializer, LocationSerializer, \
    EmissionsSourceSerializer, EmissionsSourceMonthEntrySerializer


@extend_schema(
    tags=['Companies'],
    request={'multipart/form-data': CompanySerializer}
)
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
    tags=['Brands'],
    request={'multipart/form-data': BrandSerializer}
)
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


@extend_schema(tags=['CompanyEmissionSources'])
class EmissionsSourceViewSet(viewsets.ModelViewSet):
    queryset = EmissionsSource.objects.all()
    serializer_class = EmissionsSourceSerializer


@extend_schema(tags=['CompanyEmissionSourceEntries'])
class EmissionsSourceMonthEntryViewSet(viewsets.ModelViewSet):
    queryset = EmissionsSourceMonthEntry.objects.all()
    serializer_class = EmissionsSourceMonthEntrySerializer
