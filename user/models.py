from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    AbstractUser,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
import re


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of username.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        e = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        p = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[!@#?\]]).{10,}$'

        if not email:
            raise ValueError(_('Enter email'))

        if not re.fullmatch(e, email):
            raise ValueError(_('Invalid email'))

        if not password:
            raise ValueError(_('Enter password'))

        if not re.fullmatch(p, password):
            raise ValueError(_('Password does not comply with requirements'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

    def create_clerk(self, email, password, **extra_fields):
        """
        Create and save a Clerk user with the given email and password.
        """

        e = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        p = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[!@#?\]]).{10,}$'

        if not email:
            raise ValueError(_('Enter email'))

        if not re.fullmatch(e, email):
            raise ValueError(_('Invalid email'))

        if not password:
            raise ValueError(_('Enter password'))

        if not re.fullmatch(p, password):
            raise ValueError(_('Password does not comply with requirements'))

        email = self.normalize_email(email)
        clerk = self.model(email=email, **extra_fields)
        clerk.set_password(password)
        clerk.save()

        return clerk


class User(AbstractBaseUser, PermissionsMixin):
    """Email as username field, uses the user manager"""
    AGENCY = [
        ('agency_1', 'Agency 1'),
        ('agency_2', 'Agency 2'),
        ('agency_3', 'Agency 3'),
        ('agency_4', 'Agency 4'),
    ]
    agency = models.CharField(max_length=30, choices=AGENCY)
    email = models.EmailField(max_length=255, blank=False, unique=True)
    name = models.CharField(max_length=255)
    badge = models.IntegerField(unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Clerk(AbstractUser):
    """Create a clerk user based on superuser"""
    AGENCY = [
            ('agency_1', 'Agency 1'),
            ('agency_2', 'Agency 2'),
            ('agency_3', 'Agency 3'),
            ('agency_4', 'Agency 4'),
    ]

    id = models.AutoField(primary_key=True)
    agency = models.CharField(max_length=30, choices=AGENCY)
    email = models.EmailField(max_length=255, blank=False, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
