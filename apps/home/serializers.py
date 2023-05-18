from rest_framework import serializers
from apps.home.models import (
    Section, Rules,
    Contact, Point,
)


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = (
            'id',
            'title',
            'description',
        )


class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rules
        fields = (
            'id',
            'title',
            'image',
            'description',
        )


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id',
            'address',
            'phone',
            'email',
        )


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = (
            'id',
            'location',
            'time',
            'phone',
        )
