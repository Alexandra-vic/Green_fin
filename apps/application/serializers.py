from rest_framework import serializers
from apps.application.models import Application
from apps.users.serializers import BrigadeRegistrationSerializer


class ClientApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'id',
            'started_create',
            'type',
            'comment',
        )


class ClientApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'id',
            'started_create',
            'type',
            'comment',
            'status',
            'finished_by_client',
            'operator',
        )


class OperatorApplicationSerializer(serializers.ModelSerializer):
    client_email = serializers.ReadOnlyField(source='client.email')
    client_phone = serializers.ReadOnlyField(source='client.phone')
    client_address = serializers.ReadOnlyField(source='client.address')
    brigade_status = serializers.ReadOnlyField(source='brigade.brigade_status')

    class Meta:
        model = Application
        fields = (
            'id',
            'started_create',
            'type',
            'comment',
            'status',
            'client_address',
            'client_email',
            'client_phone',
            'operator',
            'brigade',
            'brigade_status',
            'finished_application',
            'finished_by_operator',
        )


class BrigadeApplicationSerializer(serializers.ModelSerializer):
    client_email = serializers.ReadOnlyField(source='client.email')
    client_phone = serializers.ReadOnlyField(source='client.phone')
    client_address = serializers.ReadOnlyField(source='client.address')
    brigade_status = serializers.ReadOnlyField(source='brigade.brigade_status')

    class Meta:
        model = Application
        fields = (
            'id',
            'started_create',
            'type',
            'comment',
            'status',
            'client_address',
            'client_email',
            'client_phone',
            'finished_application',
            'finished_by_brigade',
            'brigade',
            'brigade_status',
        )
