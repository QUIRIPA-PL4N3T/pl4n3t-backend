from django.urls import path, include
from rest_framework.routers import DefaultRouter
from emissions.api import (
    GreenhouseGasViewSet,
    SourceTypeViewSet,
    FactorTypeViewSet,
    EmissionFactorViewSet,
    GreenhouseGasEmissionViewSet,
    SaveEmissionDataView,
)

router = DefaultRouter()

router.register(r'greenhouse-gases', GreenhouseGasViewSet)
router.register(r'source-types', SourceTypeViewSet)
router.register(r'factor-types', FactorTypeViewSet)
router.register(r'emission-factors', EmissionFactorViewSet)
router.register(r'greenhouse-gas-emissions', GreenhouseGasEmissionViewSet)

app_name = 'emissions'

api_urls = ([
    path('', include(router.urls)),
    path('save-emission-data/', SaveEmissionDataView.as_view(), name='save-emission-data'),
], 'emissions')
