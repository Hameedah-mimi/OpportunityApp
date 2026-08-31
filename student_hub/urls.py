from django.contrib import admin
from django.urls import include, path


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

    path("api/contact/", include("contact.urls")),
]