from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Application,
    SavedOpportunity,
)

from .serializers import (
    ApplicationSerializer,
    SavedOpportunitySerializer,
)


class SavedOpportunityView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        saved = SavedOpportunity.objects.filter(
            user=request.user
        )

        serializer = SavedOpportunitySerializer(
            saved,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        opportunity_id = request.data.get(
            'opportunity'
        )

        if not opportunity_id:
            return Response(
                {
                    'message': 'Opportunity ID is required.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        saved, created = (
            SavedOpportunity.objects.get_or_create(
                user=request.user,
                opportunity_id=opportunity_id
            )
        )

        if not created:
            return Response(
                {
                    'message': 'Opportunity already saved.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SavedOpportunitySerializer(
            saved
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request):

        opportunity_id = request.data.get(
            'opportunity'
        )

        deleted, _ = (
            SavedOpportunity.objects.filter(
                user=request.user,
                opportunity_id=opportunity_id
            ).delete()
        )

        if not deleted:
            return Response(
                {
                    'message': 'Saved opportunity not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                'message': 'Opportunity removed from saved list.'
            },
            status=status.HTTP_200_OK
        )


class ApplicationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        applications = Application.objects.filter(
            user=request.user
        )

        serializer = ApplicationSerializer(
            applications,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = ApplicationSerializer(
            data=request.data
        )

        if serializer.is_valid():

            application = serializer.save(
                user=request.user
            )

            if application.status == 'applied':
                application.applied_at = timezone.now()
                application.save()

            return Response(
                ApplicationSerializer(
                    application
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ApplicationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, application_id):

        try:
            application = Application.objects.get(
                id=application_id,
                user=request.user
            )
        except Application.DoesNotExist:
            return Response(
                {
                    'message': 'Application not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ApplicationSerializer(
            application,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            application = serializer.save()

            if application.status == 'applied':
                application.applied_at = timezone.now()
                application.save()

            return Response(
                ApplicationSerializer(
                    application
                ).data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )