from django.urls import path

from .views import (
    NotificationListView,
    NotificationDetailView,
)


urlpatterns = [
    path(
        '',
        NotificationListView.as_view(),
        name='notifications'
    ),

    path(
        '<int:notification_id>/',
        NotificationDetailView.as_view(),
        name='notification-detail'
    ),
]