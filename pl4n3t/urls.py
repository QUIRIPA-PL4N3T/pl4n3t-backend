"""pl4n3t URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from main.urls import api_urls as main_api_urls
from accounts.urls import api_urls as account_api_urls
from companies.urls import api_urls as companies_api_urls
from emission_source_classifications.urls import api_urls as classifications_api_urls
from emissions.urls import api_urls as emission_api_urls
from documents.urls import api_urls as documents_api_urls
from memberships.urls import api_urls as memberships_api_urls
from reports.urls import api_urls as reports_api_urls
from activities.urls import api_urls as activities_api_urls


# Create the API namespace and add the API only URLs of the applications
api_urls = ([
    path('accounts/', include(account_api_urls, namespace='accounts')),
    path('main/', include(main_api_urls, namespace='main')),
    path('companies/', include(companies_api_urls, namespace='companies')),
    path('classifications/', include(classifications_api_urls, namespace='classifications')),
    path('emissions/', include(emission_api_urls, namespace='emissions')),
    path('documents/', include(documents_api_urls, namespace='documents')),
    path('memberships/', include(memberships_api_urls, namespace='memberships')),
    path('reports/', include(reports_api_urls, namespace='reports')),
    path('activities/', include(activities_api_urls, namespace='activities')),
], 'api')

urlpatterns = [
    path('', include('main.urls')),
    path('api/', include(api_urls, namespace='api')),
    path('admin/', admin.site.urls),
    path('documentation/schema.yml', SpectacularAPIView.as_view(), name='schema'),
    path('documentation/api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('documentation/api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),
    path('account/', include('accounts.urls')),
    path('reports/', include('reports.urls')),
    path('companies/', include('companies.urls')),
]

if not settings.IS_PRODUCTION:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
