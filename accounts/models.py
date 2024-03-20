from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):

    CHOICES = (
        ("admin", "Admin"),
        ("doctor", "Doctor"),
    )
    role = models.CharField(max_length=10, choices=CHOICES, null=True)
    phone_number = models.CharField(max_length=15, default="No phone number provided")
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default="Gender not specified"
    )
