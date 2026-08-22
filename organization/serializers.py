from rest_framework import serializers
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization

        fields = [
            'id',
            'owner',
            'name',
            'description',
            'logo',
            'website',
            'location',
            'verification_status',
            'created_at',
        ]

        read_only_fields = [
            'owner',
            'verification_status',
            'created_at',
        ]