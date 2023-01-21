from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
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

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a new superuser."""

        extra_fields.setdefault('role', "ADMIN")
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        CLERK = "CLERK", 'Clerk'
        OFFICER = "OFFICER", 'Officer'

    class Agency(models.TextChoices):
        ALBANY = "albany", 'Albany'
        RICHMOND = "richmond", 'Richmond'
        SACRAMENTO = "sacramento", 'Sacramento'
        PASADENA = "pasadena", 'Pasadena'

    agency = Agency.ALBANY
    officer = Role.OFFICER

    username = None
    first_name = None
    last_name = None

    email = models.EmailField(
        max_length=255,
        blank=False,
        null=False,
        unique=True)
    name = models.CharField(max_length=255)
    agency = models.CharField(
        max_length=50,
        choices=Agency.choices,
        default=agency)
    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=officer)
    badge = models.IntegerField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.agency = self.agency
            return super().save(*args, **kwargs)


class Clerk(User):

    role = User.Role.CLERK

    class Meta:
        proxy = True


class Officer(User):

    role = User.Role.OFFICER

    class Meta:
        proxy = True
