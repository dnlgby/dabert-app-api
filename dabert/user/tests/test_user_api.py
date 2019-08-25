from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users public API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating a user with valid payload is successful"""

        # Payload for the reqest
        payload = {
            'car_id': "123-456-789",
            'email': "test@email.com",
            'phone_number': "0544444444",
            'password': "password"
        }

        # Make the api create call
        res = self.client.post(CREATE_USER_URL, payload)

        # Get the create user instance
        user = get_user_model().objects.get(**res.data)

        # 1. Check that the user is created successfully
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # 2. Check if user can log-in
        self.assertTrue(user.check_password(payload['password']))

        # 3. Check that the password is never returned with user fetching
        self.assertNotIn('password', res.data)

    def test_user_already_exists(self):
        """Test creating user with an existing cardentials is failling"""

        # Payload for the reqest
        payload = {
            'car_id': "123-456-789",
            'email': "test@email.com",
            'phone_number': "0544444444",
            'password': "password"
        }

        # Create the base user
        create_user(**payload)

        # Make the api create call
        res = self.client.post(CREATE_USER_URL, payload)

        # Check if the server is returning a bad request response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""

        # Payload for the reqest
        payload = {
            'car_id': "123-456-789",
            'email': "test@email.com",
            'phone_number': "0544444444",
            'password': "pw"
        }

        # Create the base user
        create_user(**payload)

        # Make the api create call
        res = self.client.post(CREATE_USER_URL, payload)

        # Check if the server is returning a bad request response
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
