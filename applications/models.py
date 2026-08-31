from django.db import models
from django.conf import settings


class SavedOpportunity(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='application_saved_opportunities' 
      )

    opportunity = models.ForeignKey(
        'opportunities.Opportunity',
        on_delete=models.CASCADE,
        related_name='saved_by'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'user',
            'opportunity',
        )

    def __str__(self):
        return f"{self.user.email} - {self.opportunity.title}"


class Application(models.Model):

    STATUS_CHOICES = (
        ('interested', 'Interested'),
        ('saved', 'Saved'),
        ('planning', 'Planning to Apply'),
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('interview', 'Interview'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    opportunity = models.ForeignKey(
        'opportunities.Opportunity',
        on_delete=models.CASCADE,
        related_name='applications'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='interested'
    )

    notes = models.TextField(
        blank=True
    )

    applied_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.email} - {self.opportunity.title}"