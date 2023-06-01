from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.home.models import (
    Section, Rules,
    Contact, Point,
)
from apps.home.serializers import (
    SectionSerializer, RulesSerializer,
    ContactSerializer, PointSerializer,
)


class SectionView(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAdminUser]


class RulesView(viewsets.ModelViewSet):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer
    permission_classes = [IsAdminUser]


class ContactView(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser]


class PointView(viewsets.ModelViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = [IsAdminUser]
