from django.contrib import admin
from .models import Skill, Interest, StudentProfile


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'university',
        'course',
        'graduation_year',
    )

    search_fields = (
        'user__email',
        'university',
        'course',
    )

    list_filter = (
        'graduation_year',
    )