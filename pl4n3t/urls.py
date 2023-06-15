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
from main.urls import api_urls as main_api_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from accounts.urls import api_urls as account_api_urls

# Create the API namespace and add the API only URLs of the applications
apiurls = ([
    path('accounts/', include(account_api_urls, namespace='accounts')),
    path('main/', include(main_api_urls, namespace='main')),
], 'api')

urlpatterns = [
    path('', include('main.urls')),
    path('api/', include(apiurls, namespace='api')),
    path('admin/', admin.site.urls),
    path('documentation/schema.yml', SpectacularAPIView.as_view(), name='schema'),
    path('documentation/api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('documentation/api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),
]

if not settings.IS_PRODUCTION:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
