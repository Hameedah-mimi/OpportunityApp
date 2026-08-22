from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('organization', 'Organization'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    country = models.CharField(
        max_length=100,
        blank=True
    )

    education_level = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.email