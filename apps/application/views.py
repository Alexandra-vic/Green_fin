from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters

from apps.application.models import Application
from apps.application.serializers import ApplicationSerializer
from apps.users.models import User
from apps.users.serializers import BrigadeRegistrationSerializer


class ClientApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class ClientApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        client = self.request.user
        return super().get_queryset().filter(client=client)        


class ApplicationListAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class AssignOperatorAPIView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.operator = request.user
        instance.save()
        return JsonResponse({'message': 'success'}, status=200)


class BrigadeListAPIView(generics.ListAPIView):
    queryset = User.objects.filter(user_type='BRIGADE')
    serializer_class = BrigadeRegistrationSerializer


class AddBrigadeAPIView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        brigade_id = request.data.get('brigade')


        if brigade_id:
            brigade = User.objects.filter(id=brigade_id, user_type='BRIGADE').first()
            if not brigade:
                return JsonResponse({'message': 'error', 'comment':'brigade not found'}, status=400)

            instance.brigade = brigade
            instance.save()

            return JsonResponse({'message': 'success'}, status=200)
        else:
            return JsonResponse({'message': 'error', 'comment':'field brigade is required'}, status=400)
