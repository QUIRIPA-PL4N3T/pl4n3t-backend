# general imports
from django.urls import path
from django.urls import include
from main.views import home, blog, company, contact_us, why_quantify, water_footprint, carbon_footprint, \
    plastic_footprint, footprint_levels, webinar_view
# api imports
from rest_framework import routers
from main.api import ConfigurationView, UnitOfMeasureViewSet, EconomicSectorViewSet, IndustryTypeViewSet, \
    LocationTypeViewSet, StateViewSet, CityViewSet, DocumentTypeViewSet

# api urls
router = routers.DefaultRouter()
router.register('configurations', ConfigurationView, basename='configurations')
router.register('unit-of-measure', UnitOfMeasureViewSet, basename='unit-of-measure')
router.register('economic-sector', EconomicSectorViewSet, basename='economic-sector')
router.register('industry-type', IndustryTypeViewSet, basename='industry-type')
router.register('location-type', LocationTypeViewSet, basename='location-type')
router.register('state', StateViewSet, basename='state')
router.register('city', CityViewSet, basename='city')
router.register('document-type', DocumentTypeViewSet, basename='document-type')

api_urls = ([
    path('', include(router.urls)),
], 'main')

# general urls
urlpatterns = [
    path('', home, name="home"),
    path('blog/', blog, name="blog"),
    path('contact-us', contact_us, name="contact-us"),
    path('company/', company, name="company"),
    path('why-quantify/', why_quantify, name="why-quantify"),
    path('water-footprint/', water_footprint, name="water-footprint"),
    path('carbon-footprint/', carbon_footprint, name="carbon-footprint"),
    path('plastic-footprint/', plastic_footprint, name="plastic-footprint"),
    path('footprint-levels/', footprint_levels, name="footprint-levels"),
    path('i18n/', include('django.conf.urls.i18n')),
    path('webinar/', webinar_view, name="webinar"),
]
