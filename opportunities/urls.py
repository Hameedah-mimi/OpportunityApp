from django.urls import path

from .views import (
    OpportunityListCreateView,
    OpportunityDetailView,
    OpportunityReportView,
)


urlpatterns = [
    path(
        '',
        OpportunityListCreateView.as_view(),
        name='opportunity-list'
    ),

    path(
        '<int:opportunity_id>/',
        OpportunityDetailView.as_view(),
        name='opportunity-detail'
    ),

    path(
        'report/',
        OpportunityReportView.as_view(),
        name='opportunity-report'
    ),
]