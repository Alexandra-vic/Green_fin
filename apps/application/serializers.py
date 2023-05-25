from rest_framework import serializers
from apps.application.models import Application


class ClientApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'id',
            'started_create',
            'type',
            'comment',
            'status',
            'finished_application',
            'finished_by_client',
        )


class OperatorApplicationSerializer(serializers.ModelSerializer):
    client_email = serializers.ReadOnlyField(source='client.email')
    client_phone = serializers.ReadOnlyField(source='client.phone')
    client_address = serializers.ReadOnlyField(source='client.address')
    operator_full_name = serializers.ReadOnlyField(source='operator.full_name')

    class Meta:
        model = Application
        fields = [
            'id',
            'started_create', 
            'type', 
            'comment', 
            'status',
            'client_address',
            'client_email', 
            'client_phone', 
            'operator_full_name', 
            'brigade',
            'finished_application',
            'finished_by_operator',
        ]        


class BrigadeApplicationSerializer(serializers.ModelSerializer):
    client_email = serializers.ReadOnlyField(source='client.email')
    client_phone = serializers.ReadOnlyField(source='client.phone')
    client_address = serializers.ReadOnlyField(source='client.address')

    class Meta:
        model = Application
        fields = (
            'id',
            'started_create',
            'type',
            'comment',
            'status',
            'client_email',
            'client_phone',
            'client_address',
            'finished_application',
            'finished_by_brigade',
        )
