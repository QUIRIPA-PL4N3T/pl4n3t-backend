from django.urls import path, include
from rest_framework.routers import DefaultRouter
from activities.api import ActivityViewSet

router = DefaultRouter()
router.register(r'', ActivityViewSet, basename='')

api_urls = ([
    path('', include(router.urls)),
], 'activities')


urlpatterns = []
