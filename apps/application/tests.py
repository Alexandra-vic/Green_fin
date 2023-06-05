from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

# from apps.users.models import User
from apps.application.models import Application
from apps.application.serializers import ClientApplicationSerializer


class ClientApplicationCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('client-application-create')
        self.client.force_authenticate(user=None)  # Disable authentication for the tests

    def test_create_application(self):
        data = {
            'type': 'Some type',
            'comment': 'Some comment',
            'status': 'Some status'
        }
        
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify that the application is created with the correct data
        application = Application.objects.latest('id')
        self.assertEqual(application.type, data['type'])
        self.assertEqual(application.comment, data['comment'])
        self.assertEqual(application.status, data['status'])
        self.assertEqual(application.client, self.client.user)
