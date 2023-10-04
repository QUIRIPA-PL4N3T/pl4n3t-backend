from django.urls import path, include
from rest_framework import routers
from documents.api import DocumentViewSet

documents_router = routers.DefaultRouter()
documents_router.register("", DocumentViewSet, basename="")

api_urls = ([
    path('', include(documents_router.urls)),
], 'documents')
