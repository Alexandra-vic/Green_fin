from rest_framework import serializers
from django.contrib.auth import authenticate

from apps.users.models import User


class OperatorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'full_name', 'is_operator',
            'password', 'password_confirmation',
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation', None)
        if password != password_confirmation:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            is_operator=validated_data['is_operator'],
            password=validated_data['password'],

        )
        return user


class BrigadeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'brigades_name', 'brigades_list',
            'is_brigade', 'password', 'password_confirmation',
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation', None)
        if password != password_confirmation:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            brigades_name=validated_data['brigades_name'],
            brigades_list=validated_data['brigades_list'],
            is_brigade=validated_data['is_brigade'],
            password=validated_data['password'],

        )
        return user


class ClientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'company_name', 'address',
            'phone', 'is_client', 'password',
            'password_confirmation',
        )

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.pop('password_confirmation', None)
        if password != password_confirmation:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            company_name=validated_data['company_name'],
            address=validated_data['address'],
            phone=validated_data['phone'],
            is_client=validated_data['is_client'],
            password=validated_data['password'],

        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.filter(email=email).first()

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email, password=password)

            if not user:
                message = 'Не удается войти в систему с предоставленными учетными данными.'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Должен содержать "адрес электронной почты" и "пароль".'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs


class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
        ]
