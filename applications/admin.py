from django.contrib import admin
from .models import SavedOpportunity, Application


@admin.register(SavedOpportunity)
class SavedOpportunityAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'opportunity',
        'created_at',
    )

    search_fields = (
        'user__email',
        'opportunity__title',
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'opportunity',
        'status',
        'applied_at',
        'updated_at',
    )

    list_filter = (
        'status',
        'applied_at',
    )

    search_fields = (
        'user__email',
        'opportunity__title',
    )

    ordering = (
        '-updated_at',
    )