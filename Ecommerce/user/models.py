from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):

    class UserRole(models.TextChoices):
        ADMIN = 'admin'
        USER = 'user'

    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, unique=True)
    address = models.TextField(null=True)
    phone = models.CharField(max_length=10, null=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.USER)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.email