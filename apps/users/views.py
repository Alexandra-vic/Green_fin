import jwt

from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, email=serializer.data.get('email')
        )
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class RegisterCompanyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                email=request.data['user']['email'],
                username=request.data['user']['email'],
                password=request.data['user']['password'],
                full_name=request.data['user']['full_name'],
                is_operator=False,
                is_technician=False
            )
            company = serializer.save(user=user)
            return Response(CompanySerializer(company).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegisterBrigadeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.is_operator:
            return Response({'detail': 'Only operators can register brigades'}, status=status.HTTP_403_FORBIDDEN)

        serializer = BrigadeSerializer(data=request.data)
        if serializer.is_valid():
            members = serializer.validated_data.pop('members')
            brigade = Brigade.objects.create(**serializer.validated_data)

            for member_data in members:
                member = User.objects.create_user(
                    email=member_data['email'],
                    username=member_data['email'],
                    password=member_data['password'],
                    full_name=member_data['full_name'],
                    is_operator=False,
                    is_technician=True
                )
                brigade.members.add(member)

            return Response(BrigadeSerializer(brigade).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)

        token_generator = PasswordResetTokenGenerator()
        code = token_generator.make_token(user)

        reset_request = PasswordResetRequest.objects.create(user=user, code=code)

        send_mail(
            'Запрос на сброс пароля',
            f'Ваш код для сброса пароля: {reset_request.code}',
            'noreply@example.com',
            [user.email],
            fail_silently=False
        )

        return Response({'detail': 'Код для сброса пароля был отправлен на ваш электронный адрес.'})


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        password = request.data.get('password')

        user = get_object_or_404(User, email=email)
        reset_request = get_object_or_404(PasswordResetRequest, user=user, code=code)

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, code):
            return Response({'detail': 'Неверный код сброса пароля.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        reset_request.delete()

        return Response({'detail': 'Пароль был успешно сброшен.'})