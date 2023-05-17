from rest_framework import serializers
from apps.application.models import Application, Team


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            'id',
            'type',
            'comment',
            'address',
            'date',
            'status',
            'datetime',
        )

        def get_fields(self):
            fields = super().get_fields()
            user = self.context['request'].user
            
            if not user.is_staff:
                fields['status'].read_only = True
            
            return fields