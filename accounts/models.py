from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email