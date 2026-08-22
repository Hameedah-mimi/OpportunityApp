from rest_framework import serializers

from .models import Opportunity, OpportunityReport


class OpportunitySerializer(serializers.ModelSerializer):

    organization_name = serializers.CharField(
        source='organization.name',
        read_only=True
    )

    class Meta:
        model = Opportunity

        fields = [
            'id',
            'organization',
            'organization_name',
            'title',
            'description',
            'category',
            'location',
            'deadline',
            'application_url',
            'funding_type',
            'eligibility',
            'requirements',
            'benefits',
            'skills',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'status',
            'created_at',
            'updated_at',
        ]


class OpportunityReportSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = OpportunityReport

        fields = [
            'id',
            'user',
            'opportunity',
            'reason',
            'description',
            'status',
            'created_at',
        ]

        read_only_fields = [
            'user',
            'status',
            'created_at',
        ]