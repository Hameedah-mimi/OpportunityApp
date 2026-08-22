from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'role',
        'country',
        'education_level',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'country',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'Opportunity Hub Information',
            {
                'fields': (
                    'role',
                    'country',
                    'education_level',
                )
            }
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Opportunity Hub Information',
            {
                'fields': (
                    'email',
                    'role',
                    'country',
                    'education_level',
                )
            }
        ),
    )