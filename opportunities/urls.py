from django.urls import path

from .views import (
    OpportunityListView,
    OpportunityDetailView,
    OpportunityReportCreateView,
    ImportOpportunityView,
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
        "import/",
        ImportOpportunityView.as_view(),
        name="import-opportunity",
    ),

    path(
        "import/perkcommons/",
        PerkCommonsImportView.as_view(),
        name="perkcommons-import",
    ),
]