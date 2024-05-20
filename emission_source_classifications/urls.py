from django.urls import path, include
from rest_framework.routers import DefaultRouter
from emission_source_classifications.api import QuantificationTypeViewSet, GHGScopeViewSet, ISOCategoryViewSet, \
    EmissionSourceGroupViewSet, CommonEquipmentViewSet, CommonActivityViewSet, CommonProductViewSet

router = DefaultRouter()

router.register(r'quantification-types', QuantificationTypeViewSet)
router.register(r'ghg-scopes', GHGScopeViewSet)
router.register(r'iso-categories', ISOCategoryViewSet)
router.register(r'emission-source-groups', EmissionSourceGroupViewSet)
router.register(r'equipments', CommonEquipmentViewSet)
router.register(r'activities', CommonActivityViewSet)
router.register(r'products', CommonProductViewSet)

app_name = 'classifications'

api_urls = ([
    path('', include(router.urls)),
], 'classifications')

