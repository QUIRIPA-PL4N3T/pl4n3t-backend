from django.urls import path, include
from rest_framework.routers import DefaultRouter
from companies.api import CompanyViewSet, BrandViewSet, MemberViewSet, LocationViewSet, EmissionsSourceViewSet, \
    EmissionsSourceMonthEntryViewSet, CompanyLogoViewSet, DashboardView
from companies.views import accept_invitation

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'company-logo', CompanyLogoViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'company-users', MemberViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'emission-sources', EmissionsSourceViewSet)
router.register(r'emission-source-month-entries', EmissionsSourceMonthEntryViewSet)

app_name = 'companies'

api_urls = ([
    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
], 'companies')

urlpatterns = [
    path('accept-invitation/<int:member_id>/', accept_invitation, name='accept_invitation'),
]
