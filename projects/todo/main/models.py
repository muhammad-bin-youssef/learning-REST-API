from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """(username -> required, email, password)"""
        if not username:
            raise ValueError("username is missing")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, blank=False, unique=True)
    email = models.EmailField(
        max_length=255,
        blank=False,
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email


class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.TextField()
    note = models.TextField()
    progress = models.BooleanField(default=False)
