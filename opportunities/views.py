from django.contrib.auth import get_user_model

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Opportunity
from .serializers import (
    OpportunitySerializer,
    OpportunityReportSerializer,
)
from .services import (
    import_opportunity,
    import_perkcommons_opportunity,
)


User = get_user_model()


class OpportunityListView(generics.ListAPIView):

    serializer_class = OpportunitySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        queryset = Opportunity.objects.filter(
            status="verified"
        ).order_by("-created_at")

        category = self.request.query_params.get(
            "category"
        )

        search = self.request.query_params.get(
            "search"
        )

        if category:
            queryset = queryset.filter(
                category=category
            )

        if search:
            queryset = queryset.filter(
                title__icontains=search
            )

        return queryset


class OpportunityDetailView(generics.RetrieveAPIView):

    queryset = Opportunity.objects.filter(
        status="verified"
    )

    serializer_class = OpportunitySerializer
    permission_classes = [AllowAny]


class OpportunityReportCreateView(
    generics.CreateAPIView
):

    serializer_class = OpportunityReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )


class ImportOpportunityView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            opportunity, created = import_opportunity(
                request.data,
                owner=request.user
            )

        except Exception as error:

            return Response(
                {
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": (
                    "Opportunity created."
                    if created
                    else "Opportunity already exists."
                ),
                "id": opportunity.id,
                "title": opportunity.title,
                "source": opportunity.source,
            },
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            )
        )


class PerkCommonsImportView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            opportunity, created = (
                import_perkcommons_opportunity(
                    request.data,
                    owner=request.user
                )
            )

        except Exception as error:

            return Response(
                {
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": (
                    "Opportunity imported successfully."
                    if created
                    else "Opportunity already exists."
                ),
                "id": opportunity.id,
                "title": opportunity.title,
                "source": opportunity.source,
            },
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            )
        )