# general imports
from django.urls import path
from django.urls import include
from main.views import home, blog, company, contact_us, why_quantify, water_footprint, carbon_footprint, \
    plastic_footprint
# api imports
from rest_framework import routers
from main.api import ConfigurationView

# api urls
api_router = routers.DefaultRouter()
# /api/main/configurations
api_router.register('configurations', ConfigurationView)

apiurls = ([
               # /api/main/<routers>
               path('', include(api_router.urls))
           ], 'main')

# general urls
urlpatterns = [
    path('', home, name="home"),
    path('blog/', blog, name="blog"),
    path('contact-us', contact_us, name="contact-us"),
    path('company/', company, name="company"),
    path('why-quantify', why_quantify, name="why-quantify"),
    path('water-footprint', water_footprint, name="water-footprint"),
    path('carbon-footprint', carbon_footprint, name="carbon-footprint"),
    path('plastic-footprint', plastic_footprint, name="plastic-footprint"),
]
