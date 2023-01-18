"""
User models.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from .utils import check_email


class UserManager(BaseUserManager):
    """User manager for commands and creation."""
    def create_user(self, email, password=None, **kwargs):
        """Create new user."""
        if not email:
            raise ValueError('Email must be provided')
        else:
            email = str(email).lower()
            if check_email(email) is False:
                raise ValueError('Email must be in the correct format')
        email_normalized = self.normalize_email(email)
        user = self.model(email=email_normalized.lower(), **kwargs)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **kwargs):
        """Create superuser to root the application."""
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)
        return user


class User(PermissionsMixin, AbstractBaseUser):
    """User model overwritting base user."""
    email = models.EmailField(max_length=240, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        """Get the fullname with first_name and last_name."""
        return self.first_name + self.last_name

    def __str__(self):
        return self.email
