from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class UserModelTests(TestCase):
    """The user model tests class"""

    def test_create_user_is_succesful(self):
        """test that a user creation is successful"""

        car_id = "123-456-789"
        email = "test@gmail.com"
        phone_number = "0546811111"
        password = "password"

        user = get_user_model().objects.create_user(
            car_id=car_id,
            email=email,
            phone_number=phone_number,
            password=password
        )

        self.assertEqual(user.car_id, car_id)
        self.assertEqual(user.email, email)
        self.assertEqual(user.phone_number, phone_number)
        self.assertTrue(user.check_password(password))

    def test_create_user_email_is_normalized(self):
        """Test that the created user email address is normalized"""

        car_id = "123-456-789"
        email = "test@GmAiL.com"
        phone_number = "0546811111"
        password = "password"

        user = get_user_model().objects.create_user(
            car_id=car_id,
            email=email,
            phone_number=phone_number,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_invalid_email_address_raise(self):
        """Test creating user with an invalid email raises an error"""

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                car_id="111111",
                email="invalid_email",
                phone_number="055555555",
                password="testpass"
            )
