from django.urls import path

from .views import (
    OrganizationListCreateView,
    OrganizationDetailView,
)


urlpatterns = [
    path(
        '',
        OrganizationListCreateView.as_view(),
        name='organization-list'
    ),

    path(
        '<int:organization_id>/',
        OrganizationDetailView.as_view(),
        name='organization-detail'
    ),
]