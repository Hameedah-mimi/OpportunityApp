from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Opportunity, OpportunityReport
from .serializers import (
    OpportunitySerializer,
    OpportunityReportSerializer,
)


class OpportunityListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        opportunities = Opportunity.objects.filter(
            status='verified'
        )

        category = request.query_params.get(
            'category'
        )

        location = request.query_params.get(
            'location'
        )

        funding_type = request.query_params.get(
            'funding_type'
        )

        if category:
            opportunities = opportunities.filter(
                category=category
            )

        if location:
            opportunities = opportunities.filter(
                location__icontains=location
            )

        if funding_type:
            opportunities = opportunities.filter(
                funding_type=funding_type
            )

        serializer = OpportunitySerializer(
            opportunities,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = OpportunitySerializer(
            data=request.data
        )

        if serializer.is_valid():

            opportunity = serializer.save()

            return Response(
                OpportunitySerializer(
                    opportunity
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class OpportunityDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, opportunity_id):

        try:
            opportunity = Opportunity.objects.get(
                id=opportunity_id
            )
        except Opportunity.DoesNotExist:
            return Response(
                {
                    'message': 'Opportunity not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OpportunitySerializer(
            opportunity
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class OpportunityReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = OpportunityReportSerializer(
            data=request.data
        )

        if serializer.is_valid():

            report = serializer.save(
                user=request.user
            )

            return Response(
                OpportunityReportSerializer(
                    report
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )