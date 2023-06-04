from django.http import JsonResponse

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters

from apps.application.models import Application
from apps.users.models import User
from apps.users.serializers import BrigadeRegistrationSerializer
from apps.application.serializers import (
    ClientApplicationSerializer,
    OperatorApplicationSerializer,
    BrigadeApplicationSerializer,
    ClientApplicationListSerializer,
)


class ClientApplicationCreateAPIView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ClientApplicationSerializer
    
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)      


class ApplicationListAPIView(generics.ListAPIView):
    def get_serializer_class(self):
        user = self.request.user

        if user.user_type == 'CLIENT':
            return ClientApplicationListSerializer
        elif user.user_type == 'OPERATOR':
            return OperatorApplicationSerializer
        elif user.user_type == 'BRIGADE':
            return BrigadeApplicationSerializer

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'CLIENT':
            return Application.objects.filter(client=user)
        elif user.user_type == 'OPERATOR':
            return Application.objects.filter(operator=user)
        elif user.user_type == 'BRIGADE':
            return Application.objects.filter(brigade=user.brigade_name)


class AssignOperatorAPIView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = OperatorApplicationSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.operator = request.user
        instance.save()
        return Response({'message': 'success'}, status=200)


class BrigadeStatusUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = BrigadeRegistrationSerializer
    lookup_field = 'pk'

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.brigade_status = request.data.get('brigade_status')
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BrigadeListAPIView(generics.ListAPIView):
    queryset = User.objects.filter(user_type='BRIGADE')
    serializer_class = BrigadeRegistrationSerializer


class AddBrigadeAPIView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = OperatorApplicationSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        brigade_id = request.data.get('brigade')

        if brigade_id:
            
            brigade = User.objects.filter(id=brigade_id, user_type='BRIGADE').first()

            if not brigade:
                return Response({'message': 'error', 'comment':'brigade not found'}, status=400)
            
            instance.brigade = brigade
            instance.save()

            return Response({'message': 'success'}, status=200)
        else:
            return Response({'message': 'error', 'comment':'field brigade is required'}, status=400)


class BrigadeApplicationStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = BrigadeApplicationSerializer
     
    def update(self, *args, **kwargs):
        instance = self.get_object()
        instance.status = "В процессе"
        instance.save()
        return Response({'message': 'success'}, status=200)


class ApplicationStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        user = self.request.user

        if user.user_type == 'BRIGADE':
            return BrigadeApplicationSerializer
        elif user.user_type == 'CLIENT':
            return ClientApplicationListSerializer
        elif user.user_type == 'OPERATOR':
            return OperatorApplicationSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        finished_by_brigade = serializer.validated_data.get('finished_by_brigade')
        finished_by_client = serializer.validated_data.get('finished_by_client')
        finished_by_operator = serializer.validated_data.get('finished_by_operator')

        if self.request.user.user_type == 'BRIGADE':
            if finished_by_brigade:
                instance.finished_by_brigade = True
                instance.save()

        elif self.request.user.user_type == 'CLIENT':
            if finished_by_client:
                instance.finished_by_client = True
                instance.save()

        elif self.request.user.user_type == 'OPERATOR':
            if finished_by_operator and instance.finished_by_brigade and instance.finished_by_client:
                instance.finished_by_operator = True
                instance.status = 'Выполнено'
                instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
