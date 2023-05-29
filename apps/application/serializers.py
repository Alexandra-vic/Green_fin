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
            'status',
            'client',
            'finished_application',
            'finished_by_client',
        )


class ApplicationSerializer(serializers.ModelSerializer):
    client_email = serializers.ReadOnlyField(source='client.email')
    client_phone = serializers.ReadOnlyField(source='client.phone')
    client_address = serializers.ReadOnlyField(source='client.address')

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
            'operator', 
            'brigade',
            'finished_application',
            'finished_by_operator',
        ]


class BrigadeApplicationSerializer(serializers.ModelSerializer):
    brigade = BrigadeRegistrationSerializer()

    class Meta:
        model = Application
        fields = [
            'id',
            'started_create',
            'type',
            'comment',
            'status',
            'client',
            'finished_application',
            'finished_by_brigade',
            'brigade',
        ]
# class BrigadeApplicationSerializer(serializers.ModelSerializer):
#     client_email = serializers.ReadOnlyField(source='client.email')
#     client_phone = serializers.ReadOnlyField(source='client.phone')
#     client_address = serializers.ReadOnlyField(source='client.address')

#     class Meta:
#         model = Application
#         fields = (
#             'id',
#             'started_create',
#             'type',
#             'comment',
#             'status',
#             'client_email',
#             'client_phone',
#             'client_address',
#             'finished_application',
#             'finished_by_brigade',
#         )
