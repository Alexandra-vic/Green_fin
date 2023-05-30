from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.application.models import Application
from apps.users.models import User
from apps.users.serializers import BrigadeRegistrationSerializer
from apps.application.serializers import ApplicationSerializer


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
        return self.partial_update(request, *args, **kwargs)


class BrigadeListAPIView(generics.ListAPIView):
    queryset = User.objects.filter(user_type='BRIGADE')
    serializer_class = BrigadeRegistrationSerializer


class AddBrigadeAPIView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        brigade_id = request.data.get('brigade_id') 

        if brigade_id:
            instance.brigade_id = brigade_id
            instance.save()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class BrigadeApplicationsAPIView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        brigade = self.request.user
        return super().get_queryset().filter(brigade=brigade) 


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
