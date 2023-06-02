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


class ApplicationStatusUpdateAPIView(APIView):
    def patch(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return Response({"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        role = user.user_type
        
        if role == 'BRIGADE':
            field_name = 'finished_by_brigade'
            status_value = 'Выполнено' if request.data.get(field_name) else 'В процессе'
        elif role == 'CLIENT':
            field_name = 'finished_by_client'
            status_value = 'Выполнено' if request.data.get(field_name) else 'В процессе'
        elif role == 'OPERATOR':
            field_name = 'finished_by_operator'
            status_value = 'Выполнено' if request.data.get(field_name) else 'В процессе'
        else:
            return Response({"error": "Недопустимая роль пользователя"}, status=status.HTTP_400_BAD_REQUEST)
        
        setattr(application, field_name, request.data.get(field_name))
        application.status = status_value
        application.save()
        
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)
