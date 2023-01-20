from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Create a Clerk user, Email as username field, uses the user manager"""
    AGENCY = [
        ('agency_1', 'Agency 1'),
        ('agency_2', 'Agency 2'),
        ('agency_3', 'Agency 3'),
        ('agency_4', 'Agency 4'),
    ]
    agency = models.CharField(max_length=30, choices=AGENCY)
    email = models.EmailField(max_length=255, blank=False, unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Clerk(models.Model):
    """Inherit from base class to create an Clerk"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='clerk_profile')

class Officer(models.Model):
    """Inherit from base class to create an Officer"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='officer_profile')
    badge = models.IntegerField(blank=False)
