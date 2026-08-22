from django.urls import path

from .views import (
    SavedOpportunityView,
    ApplicationListCreateView,
    ApplicationDetailView,
)


urlpatterns = [
    path(
        'saved/',
        SavedOpportunityView.as_view(),
        name='saved-opportunities'
    ),

    path(
        '',
        ApplicationListCreateView.as_view(),
        name='applications'
    ),

    path(
        '<int:application_id>/',
        ApplicationDetailView.as_view(),
        name='application-detail'
    ),
]