from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from apps.users.models import User, Brigade, Company


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'role')


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user


class OperatorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Operator
        fields = ('email', 'password', 'full_name')

    def create(self, validated_data):
        operator = Operator.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            role='OPERATOR'
        )
        return operator


class BrigadeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Brigade
        fields = ('name', 'password', 'members')

    def create(self, validated_data):
        brigade = Brigade.objects.create_user(
            name=validated_data['name'],
            password=validated_data['password'],
            members=validated_data['members'],
            role='BRIGADE'
        )
        return brigade


class ClientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = ('email', 'password', 'company_name', 'address', 'phone')

    def create(self, validated_data):
        client = Client.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            company_name=validated_data['company_name'],
            address=validated_data['address'],
            phone=validated_data['phone'],
            role='CLIENT'
        )
        return client


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            
            if not user:
                message = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = 'Must include "email" and "password".'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs