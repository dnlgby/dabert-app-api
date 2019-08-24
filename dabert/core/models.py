from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.core.validators import validate_email
from django.conf import settings



class UserManager(BaseUserManager):

    def create_user(self, car_id, email, phone_number, password=None, **extra_fields):
        """Creates and saves a new user"""

        if not car_id:
            raise ValueError("User most have a car id")

        if not email:
            raise ValueError("User most have an email address")

        if not phone_number:
            raise ValueError("User most have a phone number")

        # Normalize and validate email address
        email = self.normalize_email(email)
        validate_email(email)
        # phone_number = self.normalize_phone_number(phone_number)

        user = self.model(car_id=car_id, email=email,
                          phone_number=phone_number, **extra_fields)
        user.car_id = car_id
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, car_id, email, phone_number,
                         password=None, **extra_fields):
        """Creates and saves a new super user"""

        user = self.create_user(car_id, email, phone_number, password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using car_id instead of user_name"""

    email = models.EmailField(max_length=255, unique=True)
    car_id = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'car_id'
    REQUIRED_FIELDS = ['email', 'phone_number']


class CarType(models.Model):
    """A test model to understand django better"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
