from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=200, unique=True)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password', 'phone_number']

