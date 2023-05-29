from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.application.models import Application
from apps.users.models import User
from apps.application.serializers import(
    ClientApplicationSerializer,
    ApplicationSerializer,
    BrigadeApplicationSerializer,
    # BrigadeApplicationSerializer,
)


class ClientApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ClientApplicationSerializer

    def get_queryset(self):
        client = self.request.user
        return super().get_queryset().filter(client=client)


class ClientApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ClientApplicationSerializer
    
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class ApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class ApplicationUpdateView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.operator = request.user
        instance.save()
        return self.partial_update(request, *args, **kwargs)


class ApplicationAssignBrigadeView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        brigade_id = request.data.get('brigade_id')
        brigade = User.objects.get(id=brigade_id)
        instance.user = brigade
        instance.save()
        return self.partial_update(request, *args, **kwargs)


class UpdateApplicationStatusView(APIView):
    def patch(self, request, pk):
        application = Application.objects.get(pk=pk)
        serializer = BrigadeApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
