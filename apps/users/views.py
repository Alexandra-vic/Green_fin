from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User
from apps.users.serializers import (
    OperatorRegistrationSerializer, BrigadeRegistrationSerializer,
    ClientRegistrationSerializer, UserLoginSerializer, ResetPasswordSerializer
)


class OperatorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.is_operator
        return True


class OperatorListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ClientRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class OperatorRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = OperatorRegistrationSerializer
    permission_classes = [OperatorPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class OperatorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = OperatorRegistrationSerializer
    permission_classes = [OperatorPermission]


class BrigadeRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = BrigadeRegistrationSerializer
    permission_classes = [OperatorPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class BrigadeListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = BrigadeRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class BrigadeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = BrigadeRegistrationSerializer
    permission_classes = [OperatorPermission]


class ClientRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ClientRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class ClientListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ClientRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ClientRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if not user.is_active:
            return Response(
                {'error': 'Учетная запись пользователя отключена.'},
                status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class ResetPasswordAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {'error': 'Пользователь с данным электронным адресом не найден'}, status=400
                )
            password = User.objects.make_random_password()
            user.set_password(password)
            user.save()
            send_mail(
                'Password Reset Request',
                f'Ваш новый пароль  {password}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response({'success': 'Отправлено электронное письмо для сброса пароля'})
        return Response({'error': 'Поле электронной почты обязательно для заполнения'}, status=400)
