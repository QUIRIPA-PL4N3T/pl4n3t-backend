from django.urls import path, include
from rest_framework.routers import DefaultRouter
from emission_source_classifications.api import QuantificationTypeViewSet, GHGScopeViewSet, ISOCategoryViewSet, \
    EmissionSourceGroupViewSet, CommonEquipmentViewSet, CommonActivityViewSet, CommonProductViewSet, InvestmentViewSet, \
    EmissionCalculatorView

router = DefaultRouter()

router.register(r'quantification-types', QuantificationTypeViewSet)
router.register(r'ghg-scopes', GHGScopeViewSet)
router.register(r'iso-categories', ISOCategoryViewSet)
router.register(r'emission-source-groups', EmissionSourceGroupViewSet)
router.register(r'equipments', CommonEquipmentViewSet)
router.register(r'activities', CommonActivityViewSet)
router.register(r'products', CommonProductViewSet)
router.register(r'investment', InvestmentViewSet)


app_name = 'classifications'

api_urls = ([
    path('', include(router.urls)),
    path('calculate/', EmissionCalculatorView.as_view(), name='calculate-emissions'),
], 'classifications')

