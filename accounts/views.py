from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)
from django.contrib.auth.tokens import default_token_generator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from firebase_admin import auth

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    ProfileSerializer,
)
User = get_user_model()


# ==========================================
# REGISTER
# ==========================================

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "message": "Account created successfully.",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                        "country": user.country,
                        "education_level": user.education_level,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================================
# NORMAL LOGIN
# ==========================================

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Login successful",

                    "access": str(refresh.access_token),

                    "refresh": str(refresh),

                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                        "country": user.country,
                        "education_level": user.education_level,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )




class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        print("GOOGLE REQUEST DATA:", request.data)

        id_token = request.data.get("idToken")

        print("ID TOKEN:", id_token)

        if not id_token:
            return Response(
                {
                    "error": "ID token is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )



        try:

            # Verify Firebase token
            decoded_token = auth.verify_id_token(id_token)

            email = decoded_token.get("email")
            name = decoded_token.get("name", "")
            firebase_uid = decoded_token.get("uid")

            if not email:

                return Response(
                    {
                        "error": "Google account has no email."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Find existing Django user
            user = User.objects.filter(
                email=email
            ).first()

            # Create user if they don't already exist
            if not user:

                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=name,
                    role="student",
                )

            # Create Django JWT
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Google login successful.",

                    "access": str(refresh.access_token),

                    "refresh": str(refresh),

                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "name": user.first_name,
                        "role": user.role,
                        "country": user.country,
                        "education_level": user.education_level,
                        "firebase_uid": firebase_uid,
                    }
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "error": "Google authentication failed.",
                    "details": str(e),
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


# ==========================================
# LOGOUT
# ==========================================

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        return Response(
            {
                "message": "Logout successful."
            },
            status=status.HTTP_200_OK
        )




class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data["email"]

        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = default_token_generator.make_token(user)

        reset_link = (
            f"http://localhost:5173/reset-password/"
            f"{uid}/{token}/"
        )

        send_mail(
            subject="Student Opportunity Hub Password Reset",

            message=(
                "Use the following link to reset your password:\n\n"
                f"{reset_link}"
            ),

            from_email=None,

            recipient_list=[
                user.email
            ],

            fail_silently=False,
        )

        return Response(
            {
                "message": "Password reset link has been sent to your email."
            },
            status=status.HTTP_200_OK
        )




class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        password = serializer.validated_data["password"]

        try:

            user_id = force_str(
                urlsafe_base64_decode(uid)
            )

            user = User.objects.get(
                pk=user_id
            )

        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist
        ):

            return Response(
                {
                    "error": "Invalid password reset link."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(
            user,
            token
        ):

            return Response(
                {
                    "error": "Invalid or expired password reset token."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(password)
        user.save()

        return Response(
            {
                "message": "Password reset successfully."
            },
            status=status.HTTP_200_OK
        )



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = ProfileSerializer(request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request):

        serializer = ProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "message": "Profile updated successfully.",
                    "user": serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )