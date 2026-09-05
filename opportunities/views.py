from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Opportunity,
    OpportunityReport,
    SavedOpportunity,
)

from .serializers import (
    OpportunitySerializer,
    OpportunityReportSerializer,
    SavedOpportunitySerializer,
)

from .services import (
    import_perkcommons_opportunity,
)

from notifications.models import Notification


User = get_user_model()


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Opportunity
from .serializers import OpportunitySerializer


class OpportunityListView(APIView):

    def get(self, request):
        opportunities = Opportunity.objects.all()
        serializer = OpportunitySerializer(opportunities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OpportunitySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class OpportunityDetailView(generics.RetrieveAPIView):

    queryset = Opportunity.objects.filter(
        status="verified"
    )

    serializer_class = OpportunitySerializer
    permission_classes = [AllowAny]


class OpportunityReportCreateView(generics.CreateAPIView):

    serializer_class = OpportunityReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


class SavedOpportunityListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        saved = SavedOpportunity.objects.filter(
            user=request.user
        ).select_related("opportunity")

        serializer = SavedOpportunitySerializer(
            saved,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        opportunity_id = request.data.get("opportunity")

        if not opportunity_id:
            return Response(
                {
                    "message": "Opportunity ID is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            opportunity = Opportunity.objects.get(
                id=opportunity_id,
                status="verified"
            )
        except Opportunity.DoesNotExist:

            return Response(
                {
                    "message": "Opportunity not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        saved, created = SavedOpportunity.objects.get_or_create(
            user=request.user,
            opportunity=opportunity
        )

        serializer = SavedOpportunitySerializer(saved)

        return Response(
            {
                "message": (
                    "Opportunity saved."
                    if created
                    else "Opportunity already saved."
                ),
                "saved": True,
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
            if created
            else status.HTTP_200_OK
        )


class SavedOpportunityDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, opportunity_id):

        deleted, _ = SavedOpportunity.objects.filter(
            user=request.user,
            opportunity_id=opportunity_id
        ).delete()

        if deleted == 0:

            return Response(
                {
                    "message": "Opportunity was not saved."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "message": "Opportunity removed from saved opportunities.",
                "saved": False
            },
            status=status.HTTP_200_OK
        )


class PerkCommonsImportView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        opportunity, created = (
            import_perkcommons_opportunity(request.data)
        )

        if opportunity is None:

            return Response(
                {
                    "message": "Invalid PerkCommons data."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if created:

            users = User.objects.filter(
                is_active=True
            )

            notifications = []

            for user in users:

                notifications.append(
                    Notification(
                        user=user,
                        title="New Opportunity Available",
                        message=(
                            f"{opportunity.title} "
                            "has just been added to Opportuna."
                        )
                    )
                )

            Notification.objects.bulk_create(
                notifications
            )

            return Response(
                {
                    "message": "Opportunity imported successfully.",
                    "id": opportunity.id,
                    "title": opportunity.title,
                    "source": "PerkCommons",
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "message": "Opportunity already exists.",
                "id": opportunity.id,
                "title": opportunity.title,
            },
            status=status.HTTP_200_OK
        )