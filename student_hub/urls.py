from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'api/auth/',
        include('accounts.urls')
    ),

    path(
        'api/profile/',
        include('profiles.urls')
    ),

    path(
        'api/organizations/',
        include('organization.urls')
    ),

    path(
        'api/opportunities/',
        include('opportunities.urls')
    ),

    path(
        'api/applications/',
        include('applications.urls')
    ),

    path(
        'api/notifications/',
        include('notifications.urls')
    ),

    path(
        'api/contact/',
        include('contact.urls')
    ),

    # Swagger / OpenAPI
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),

    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema'
        ),
        name='swagger-ui'
    ),
]