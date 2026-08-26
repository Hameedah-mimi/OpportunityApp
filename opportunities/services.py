from django.contrib.auth import get_user_model
from django.utils.dateparse import parse_date, parse_datetime
from django.utils import timezone
from django.utils.text import slugify

from .models import Opportunity
from organization.models import Organization


User = get_user_model()


def parse_deadline(value):
    if not value:
        return None

    parsed_datetime = parse_datetime(str(value))

    if parsed_datetime:
        if timezone.is_naive(parsed_datetime):
            parsed_datetime = timezone.make_aware(parsed_datetime)

        return parsed_datetime

    parsed_date = parse_date(str(value))

    if parsed_date:
        return timezone.make_aware(
            timezone.datetime.combine(
                parsed_date,
                timezone.datetime.min.time()
            )
        )

    return None


def get_or_create_organization(data, owner=None):
    organization_name = (
        data.get("provider")
        or data.get("organization_name")
        or "Unknown Organization"
    )

    organization = Organization.objects.filter(
        name=organization_name
    ).first()

    if organization:
        return organization

    if owner is None:
        owner = User.objects.filter(
            is_active=True
        ).order_by("id").first()

    if owner is None:
        raise ValueError(
            "A user is required to create the organization."
        )

    organization = Organization.objects.create(
        owner=owner,
        name=organization_name,
        description="Organization imported from PerkCommons.",
        website=data.get("officialUrl", ""),
        location=", ".join(data.get("regions", [])),
    )

    return organization


def import_perkcommons_opportunity(data, owner=None):

    organization = get_or_create_organization(
        data,
        owner=owner
    )

    category = data.get(
        "category",
        ""
    ).lower()

    category_map = {
        "awards-recognition": "competition",
        "competitions": "competition",
        "competition": "competition",
        "internships": "internship",
        "internship": "internship",
        "fellowships": "fellowship",
        "fellowship": "fellowship",
        "scholarships": "scholarship",
        "scholarship": "scholarship",
        "grants": "grant",
        "grant": "grant",
        "hackathons": "hackathon",
        "hackathon": "hackathon",
    }

    category = category_map.get(
        category,
        "other"
    )

    title = data.get(
        "title",
        "Untitled Opportunity"
    )

    external_id = (
        data.get("id")
        or data.get("external_id")
    )

    if not external_id:
        external_id = slugify(
            f"{organization.name}-{title}"
        )

    application_url = (
        data.get("officialUrl")
        or data.get("sourceUrl")
        or data.get("application_url")
        or ""
    )

    deadline = parse_deadline(
        data.get("deadline")
    )

    opportunity, created = Opportunity.objects.update_or_create(
        external_id=external_id,
        defaults={
            "organization": organization,
            "title": title,
            "description": data.get(
                "description",
                ""
            ),
            "category": category,
            "location": ", ".join(
                data.get("regions", [])
            ),
            "deadline": deadline,
            "application_url": application_url,
            "funding_type": data.get(
                "funding_type",
                "unfunded"
            ),
            "eligibility": data.get(
                "eligibility",
                ""
            ),
            "requirements": data.get(
                "requirements",
                ""
            ),
            "benefits": data.get(
                "value",
                ""
            ),
            "status": "verified",
            "source": "PerkCommons",
            "source_url": data.get(
                "sourceUrl",
                ""
            ),
            "external_id": external_id,
        }
    )

    return opportunity, created


def import_opportunity(data=None, **kwargs):
    """
    General opportunity importer.
    """

    if data is None:
        data = kwargs

    return import_perkcommons_opportunity(
        data
    )