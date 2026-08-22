from django.urls import path

from .views import (
    StudentProfileView,
    SkillListView,
    InterestListView,
)


urlpatterns = [
    path(
        '',
        StudentProfileView.as_view(),
        name='student-profile'
    ),

    path(
        'skills/',
        SkillListView.as_view(),
        name='skills'
    ),

    path(
        'interests/',
        InterestListView.as_view(),
        name='interests'
    ),
]