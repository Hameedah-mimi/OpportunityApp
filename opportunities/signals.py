from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Opportunity
from notifications.models import Notification


User = get_user_model()


@receiver(post_save, sender=Opportunity)
def create_opportunity_notification(
    sender,
    instance,
    created,
    **kwargs
):

    if not created:
        return

    if instance.status != "verified":
        return

    users = User.objects.filter(
        is_active=True
    )

    notifications = []

    for user in users:

        notifications.append(
            Notification(
                user=user,
                title="New Opportunity Available",
                message=(
                    f"{instance.title} has just been "
                    f"added to Opportuna."
                )
            )
        )

    Notification.objects.bulk_create(
        notifications
    )