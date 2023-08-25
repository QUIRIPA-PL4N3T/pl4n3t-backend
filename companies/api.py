from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from companies.models import Company, Brand, CompanyUser, Location, EmissionsSource, EmissionsSourceMonthEntry
from companies.serializers import CompanySerializer, BrandSerializer, CompanyUserSerializer, LocationSerializer, \
    EmissionsSourceSerializer, EmissionsSourceMonthEntrySerializer


@extend_schema(tags=['Companies'])
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


@extend_schema(tags=['Brands'])
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


@extend_schema(tags=['CompanyUsers'])
class CompanyUserViewSet(viewsets.ModelViewSet):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanyUserSerializer


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
