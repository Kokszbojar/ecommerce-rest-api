from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.models import User
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers, serializers, viewsets

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include('restapi.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
