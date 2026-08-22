from django.contrib import admin
from .models import Opportunity, OpportunityReport


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'organization',
        'category',
        'location',
        'deadline',
        'funding_type',
        'status',
        'created_at',
    )

    list_filter = (
        'category',
        'funding_type',
        'status',
        'location',
    )

    search_fields = (
        'title',
        'description',
        'organization__name',
    )

    ordering = (
        '-created_at',
    )


@admin.register(OpportunityReport)
class OpportunityReportAdmin(admin.ModelAdmin):

    list_display = (
        'opportunity',
        'user',
        'reason',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'opportunity__title',
        'user__email',
        'reason',
    )