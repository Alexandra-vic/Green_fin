from rest_framework import generics
from django.shortcuts import get_object_or_404

from apps.application.models import Application
from apps.application.serializers import(
    ClientApplicationSerializer,
    OperatorApplicationSerializer,
    BrigadeApplicationSerializer,
)


class ClientApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ClientApplicationSerializer


class ClientApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ClientApplicationSerializer


class OperatorApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = OperatorApplicationSerializer


class OperatorApplicationUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = OperatorApplicationSerializer

    @staticmethod
    def start_work(request, application_id):
        application = get_object_or_404(Application, id=application_id)
        operator = request.user
        application.operator = operator
        application.save()


class BrigadeApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = BrigadeApplicationSerializer


class BrigadeApplicationUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = BrigadeApplicationSerializer
