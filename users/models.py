"""This file declare database schema"""
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class LeluUserManager(UserManager):
    "LeluUserManager is customize manager for LeluUser model"

    def _create_user(self, email, name, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, name, password, **extra_fields)
    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, name, password, **extra_fields)


class LeluUser(AbstractUser):
    """LeluUser specify custom user model to use as AUTH_USER_MODEL"""

    username = None
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=200)
    objects = LeluUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.email
