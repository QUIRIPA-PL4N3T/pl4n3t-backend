from django.urls import path, include
from rest_framework.routers import DefaultRouter
from companies.api import CompanyViewSet, BrandViewSet, MemberViewSet, LocationViewSet, EmissionsSourceViewSet, \
    CompanyLogoViewSet, DashboardView
from companies.views import accept_invitation

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'company-logo', CompanyLogoViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'emission-sources', EmissionsSourceViewSet)

app_name = 'companies'

api_urls = ([
    path('', include(router.urls)),
    path('companies/<int:company_id>/members/', include([
        path('<int:pk>/', MemberViewSet.as_view(
            {'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
             name='member-detail'),
    ])),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

], 'companies')

urlpatterns = [
    path('accept-invitation/<int:member_id>/', accept_invitation, name='accept-invitation'),
]
