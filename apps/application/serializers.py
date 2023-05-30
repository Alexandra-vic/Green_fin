from rest_framework import serializers
from apps.application.models import Application
from apps.users.serializers import BrigadeRegistrationSerializer


# class ClientApplicationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Application
#         fields = (
#             'id',
#             'started_create',
#             'type',
#             'comment',
#             'status',
#             'client',
#             'finished_application',
#             'finished_by_client',
#         )


class ApplicationSerializer(serializers.ModelSerializer):
    client_email = serializers.ReadOnlyField(source='client.email')
    client_phone = serializers.ReadOnlyField(source='client.phone')
    client_address = serializers.ReadOnlyField(source='client.address')

    def __init__(self, *args, **kwargs):
        user = kwargs['context']['request'].user

        if user.user_type == 'CLIENT':
            fields = [
                'id',
                'started_create',
                'type',
                'comment',
                'status',
                'client_address',
                'client_email',
                'client_phone',
                'finished_application',
                'finished_by_client',
            ]
        elif user.user_type == 'OPERATOR':
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
        elif user.user_type == 'BRIGADE':
            fields = [
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
            ]
        else:
            fields = [
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
                'finished_by_client',
                'finished_by_operator',
                'brigade',
            ]

        super().__init__(*args, **kwargs)
        self.fields = {field_name: self.fields[field_name] for field_name in fields}

    class Meta:
        model = Application
        fields = '__all__'


# class BrigadeApplicationSerializer(serializers.ModelSerializer):
#     client_email = serializers.ReadOnlyField(source='client.email')
#     client_phone = serializers.ReadOnlyField(source='client.phone')
#     client_address = serializers.ReadOnlyField(source='client.address')

#     class Meta:
#         model = Application
#         fields = [
#             'id',
#             'started_create',
#             'type',
#             'comment',
#             'status',
#             'client_address',
#             'client_email', 
#             'client_phone',
#             'finished_application',
#             'finished_by_brigade',
#             'brigade',
#         ]
        
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
