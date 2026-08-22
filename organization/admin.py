from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'owner',
        'verification_status',
        'location',
        'created_at',
    )

    list_filter = (
        'verification_status',
        'created_at',
    )

    search_fields = (
        'name',
        'owner__email',
        'location',
    )