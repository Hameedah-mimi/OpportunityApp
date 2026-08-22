from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import StudentProfile, Skill, Interest
from .serializers import (
    StudentProfileSerializer,
    SkillSerializer,
    InterestSerializer,
)


class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = StudentProfile.objects.get(
                user=request.user
            )
        except StudentProfile.DoesNotExist:
            return Response(
                {
                    'message': 'Student profile not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentProfileSerializer(profile)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request):
        try:
            profile = StudentProfile.objects.get(
                user=request.user
            )
        except StudentProfile.DoesNotExist:
            return Response(
                {
                    'message': 'Student profile not found.'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StudentProfileSerializer(
            profile,
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


class SkillListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        skills = Skill.objects.all()

        serializer = SkillSerializer(
            skills,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class InterestListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        interests = Interest.objects.all()

        serializer = InterestSerializer(
            interests,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )