from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import ContactMessage
from .serializers import ContactMessageSerializer


class ContactMessageCreateView(generics.CreateAPIView):

    queryset = ContactMessage.objects.all()

    serializer_class = ContactMessageSerializer

    permission_classes = [AllowAny]