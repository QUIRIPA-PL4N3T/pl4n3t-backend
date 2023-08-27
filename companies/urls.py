from django.urls import path, include
from rest_framework.routers import DefaultRouter
from companies.api import CompanyViewSet, BrandViewSet, MemberViewSet, LocationViewSet, EmissionsSourceViewSet, EmissionsSourceMonthEntryViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'company-users', MemberViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'emission-sources', EmissionsSourceViewSet)
router.register(r'emission-source-month-entries', EmissionsSourceMonthEntryViewSet)

app_name = 'companies'

api_urls = ([
    path('', include(router.urls)),
], 'companies')

