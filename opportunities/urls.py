from django.urls import path

from .views import (
    OpportunityListView,
    OpportunityDetailView,
    OpportunityReportCreateView,
    SavedOpportunityListView,
    SavedOpportunityDeleteView,
    PerkCommonsImportView,
)


urlpatterns = [

    path(
        "",
        OpportunityListView.as_view(),
        name="opportunity-list",
    ),

    path(
        "<int:pk>/",
        OpportunityDetailView.as_view(),
        name="opportunity-detail",
    ),

    path(
        "<int:pk>/report/",
        OpportunityReportCreateView.as_view(),
        name="opportunity-report",
    ),

    path(
        "saved/",
        SavedOpportunityListView.as_view(),
        name="saved-opportunities",
    ),

    path(
        "saved/<int:opportunity_id>/",
        SavedOpportunityDeleteView.as_view(),
        name="delete-saved-opportunity",
    ),

    path(
        "import/perkcommons/",
        PerkCommonsImportView.as_view(),
        name="perkcommons-import",
    ),
]