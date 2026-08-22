from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        organizations = Organization.objects.all()

        serializer = OrganizationSerializer(
            organizations,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):

        serializer = OrganizationSerializer(
            data=request.data
        )

        if serializer.is_valid():

            organization = serializer.save(
                owner=request.user
            )

            return Response(
                OrganizationSerializer(
                    organization
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class OrganizationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, organization_id):

        try:
            return Organization.objects.get(
                id=organization_id
            )

        except Organization.DoesNotExist:
            return None

    def get(self, request, organization_id):

        organization = self.get_object(
            organization_id
        )

        if organization is None:
            return Response(
                {
                    'message': 'Organization not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = OrganizationSerializer(
            organization
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, organization_id):

        organization = self.get_object(
            organization_id
        )

        if organization is None:
            return Response(
                {
                    'message': 'Organization not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if organization.owner != request.user:
            return Response(
                {
                    'message': 'You can only edit your own organization.'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = OrganizationSerializer(
            organization,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )