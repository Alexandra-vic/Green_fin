from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.application.models import Application
from apps.application.serializers import ApplicationSerializer


class ApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer 
    permission_classes = [IsAuthenticated]


class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAdminUser]
