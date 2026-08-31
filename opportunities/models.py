from django.db import models

from django.db import models
from django.conf import settings


class Opportunity(models.Model):

    CATEGORY_CHOICES = (
        ('scholarship', 'Scholarship'),
        ('grant', 'Grant'),
        ('fellowship', 'Fellowship'),
        ('internship', 'Internship'),
        ('graduate_program', 'Graduate Program'),
        ('apprenticeship', 'Apprenticeship'),
        ('hackathon', 'Hackathon'),
        ('competition', 'Competition'),
        ('startup', 'Startup Competition'),
        ('workshop', 'Workshop'),
        ('conference', 'Conference'),
        ('volunteer', 'Volunteer Program'),
        ('leadership', 'Leadership Program'),
        ('other', 'Other'),
    )

    FUNDING_CHOICES = (
        ('fully_funded', 'Fully Funded'),
        ('partially_funded', 'Partially Funded'),
        ('unfunded', 'Unfunded'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('verified', 'Verified'),
        ('reported', 'Reported'),
        ('rejected', 'Rejected'),
    )

    organization = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        related_name='opportunities'
    )

    title = models.CharField(max_length=255)

    description = models.TextField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    deadline = models.DateTimeField(
    null=True,
    blank=True
)

    application_url = models.URLField()

    funding_type = models.CharField(
        max_length=30,
        choices=FUNDING_CHOICES,
        default='unfunded'
    )

    eligibility = models.TextField(
        blank=True
    )

    requirements = models.TextField(
        blank=True
    )

    benefits = models.TextField(
        blank=True
    )

    skills = models.ManyToManyField(
        'profiles.Skill',
        blank=True,
        related_name='opportunities'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    source = models.CharField(
        max_length=100,
        blank=True
    )

    source_url = models.URLField(
        blank=True
    )

    external_id = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

class SavedOpportunity(models.Model):

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='saved_opportunities'
    )

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name='saved_by_users'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'opportunity'],
                name='unique_saved_opportunity'
            )
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} saved {self.opportunity.title}"


class OpportunityReport(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    )

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='opportunity_reports'
    )

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name='reports'
    )

    reason = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Report - {self.opportunity.title}"

class Organization(models.Model):
    
    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    website = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

class Meta:
    app_label = 'organization'
