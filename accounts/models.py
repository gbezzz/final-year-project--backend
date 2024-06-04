from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):

    CHOICES = (
        ("admin", "Admin"),
        ("doctor", "Doctor"),
    )
    role = models.CharField(max_length=10, choices=CHOICES, null=True)
    phone_number = models.CharField(max_length=150, default="0000")
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    gender = models.CharField(
        max_length=150, choices=GENDER_CHOICES, default="Gender not specified"
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
