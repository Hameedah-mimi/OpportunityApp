from django.db import models
from django.conf import settings


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    university = models.CharField(max_length=200, blank=True)
    course = models.CharField(max_length=200, blank=True)

    graduation_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    languages = models.CharField(
        max_length=300,
        blank=True
    )

    bio = models.TextField(blank=True)

    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)

    cv = models.FileField(
        upload_to='cvs/',
        blank=True,
        null=True
    )

    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name='students'
    )

    interests = models.ManyToManyField(
        Interest,
        blank=True,
        related_name='students'
    )

    def __str__(self):
        return f"{self.user.email} Profile"