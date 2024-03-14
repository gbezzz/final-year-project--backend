from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=100)
    CHOICES = (
        ("admin", "Admin"),
        ("doctor", "Doctor"),
    )
    role = models.CharField(max_length=10, choices=CHOICES, null=True)
