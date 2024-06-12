from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    user_id = models.CharField(max_length=8, unique=True)
    phone_number = models.CharField(max_length=15, default=" ")

    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="customuser_groups",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="customuser_user_permissions",
        related_query_name="customuser",
    )
