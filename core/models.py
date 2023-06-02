from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=200, unique=True)
    username = models.CharField(max_length=150, unique=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=None,blank=True)
    points = models.IntegerField(default=0)
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password', 'phone_number']

