from django.db import models
from django.conf import settings


class Organization(models.Model):

    VERIFICATION_STATUS = (
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organizations'
    )

    name = models.CharField(max_length=200)

    description = models.TextField()

    logo = models.ImageField(
        upload_to='organizations/',
        blank=True,
        null=True
    )

    website = models.URLField(blank=True)

    location = models.CharField(
        max_length=200,
        blank=True
    )

    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name