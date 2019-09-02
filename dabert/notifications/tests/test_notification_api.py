from django.test import TestCase
from django.urls import reverse
from django.settings import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


NOTIFICATIONS_URL = reverse('notifications:notification-list')


class PublicNotificationsApiTests(TestCase):
    """Test the notifications public API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to use API"""

        res = self.client.get(NOTIFICATIONS_URL)

        # Check that the request is unauthotized
        self.assertEqual(res.status, status.HTTP_401_UNAUTHORIZED)


class PrivateNotificationsApiTests(TestCase):
    """Test the authorized private notifications API"""

    def setUp(self):

        # Payload for user creation
        payload = {
            'car_id': "123-456-789",
            'email': "test@email.com",
            'phone_number': "0544444444",
            'password': "password"
        }

        # Create the user
        self.user = get_user_model().objects.create_user(**payload)

        # Create the API to use.
        self.client = APIClient()

        # Authenticate the newly created user
        self.client.force_authenticate(self.user)

    def test_getting_notifications(self):
        """Test get list of notifications is success"""

        res = self.client.get(NOTIFICATIONS_URL)

        # Result code for request is success
        self.assertEqual(res.status, status_code.HTTP_200_OK)
