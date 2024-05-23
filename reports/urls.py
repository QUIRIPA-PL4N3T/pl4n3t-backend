from django.urls import path
from reports.views import ReportPDFDetailView, PrintView, DownloadView, DynamicNameView
from reports.api import ReportTemplateViewSet, CompanyTemplateViewSet, ReportViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'planet-templates', ReportTemplateViewSet)
router.register(r'company-templates', CompanyTemplateViewSet)
router.register(r'reports', ReportViewSet)

api_urls = ([
    path('', include(router.urls)),
], 'reports')

urlpatterns = [
    path('pdf/<int:pk>/', ReportPDFDetailView.as_view(), name='report-pdf'),
    path('print/<int:pk>/', PrintView.as_view(), name='print_view'),
    path('download/<int:pk>/', DownloadView.as_view(), name='download_view'),
    path('dynamic/<int:pk>/', DynamicNameView.as_view(), name='dynamic_name_view'),
]
