from rest_framework import serializers

from .models import (
    Application,
    SavedOpportunity,
)


class SavedOpportunitySerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = SavedOpportunity

        fields = [
            'id',
            'user',
            'opportunity',
            'created_at',
        ]

        read_only_fields = [
            'user',
            'created_at',
        ]


class ApplicationSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Application

        fields = [
            'id',
            'user',
            'opportunity',
            'status',
            'notes',
            'applied_at',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'user',
            'created_at',
            'updated_at',
        ]