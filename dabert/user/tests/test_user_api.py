from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


# Public tests
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

    def test_create_token_for_user_is_succesful(self):
        """Test that a token is created for the user"""

        # Payload for the reqest
        create_user_params = {
            'car_id': "123-456-789",
            'email': "test@email.com",
            'phone_number': "0544444444",
            'password': "password"
        }

        # Create the base user
        create_user(**create_user_params)

        # Payload for the reqest
        payload = {
            'car_id': "123-456-789",
            'password': "password"
        }

        # Make the api get token call
        res = self.client.post(TOKEN_URL, payload)

        # Response ok and token retrieved
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_cardentials_is_failing(self):
        """Test that providing a bad cardentials while requesting token
           will fail"""

        # User creation params
        create_user_params = {
            'car_id': "123-456-789",
            'email': "test@email.com",
            'phone_number': "0544444444",
            'password': "password"
        }

        # Creating the user
        create_user(**create_user_params)

        # Login Payload
        payload = {
            'car_id': "123-456-789",
            'password': "wrong_password"
        }

        # Make the request for the token with invalid cardentials
        res = self.client.post(TOKEN_URL, payload)

        # No token retrieved and request is invalid
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_user_not_exists_is_failing(self):
        """Test that creating a token for not existing user if failing"""

        # Login Payload
        payload = {
            'car_id': "123-456-789",
            'password': "password"
        }

        # Make the request for the token with not existing user
        res = self.client.post(TOKEN_URL, payload)

        # No token retrieved and request is invalid
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""

        # Login Payload
        payload = {
            'car_id': "123-456-789",
            'password': ""
        }

        # Make the request for the token with empty field.
        res = self.client.post(TOKEN_URL, payload)

        # No token retrieved and request is invalid
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Private tests
class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        """Set up before tests"""

        # Create class testing user
        create_user_params = {
            'car_id': "123-456-789",
            'email': "test@email.com",
            'phone_number': "0544444444",
            'password': "password"
        }
        self.user = create_user(**create_user_params)

        self.client = APIClient()

        # Login with the newly created user
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retreiving profile for logged in user is successful"""

        res = self.client.get(ME_URL)

        # Check that the profile is rerteived successfully
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'car_id': self.user.car_id,
            'email': self.user.email,
            'phone_number': self.user.phone_number
        })

    def test_post_me_not_allowed(self):
        """Test the posting in me is not allowed"""

        # Try to post
        res = self.client.post(ME_URL, {})

        # Verify that the response code is 405 - not allowed
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile is successful"""

        # Updating params
        update_user_params = {
            'car_id': "111111111",
            'email': "test_new@email.com",
            'password': "new_password"
        }

        # Make the patch request
        res = self.client.patch(ME_URL, update_user_params)

        # Refresh the user instance from the database
        self.user.refresh_from_db()

        # Check that the user is updated successfully
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.car_id, update_user_params['car_id'])
        self.assertEqual(self.user.email, update_user_params['email'])
        self.assertTrue(
            self.user.check_password(update_user_params['password'])
        )
