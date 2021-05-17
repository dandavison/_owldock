import os
import sys
from itertools import chain

from django.contrib.auth import get_user_model
from django.db.transaction import atomic

from app.models import (
    Country,
    User,
)
from client.models import (
    Client,
    Applicant,
    ApplicantNationality,
)
from owldock.utils import strip_prefix


@atomic
def create_fake_applicants() -> None:
    print("Creating applicants")
    all_countries = list(Country.objects.all())
    belgium = Country.objects.get(name="Belgium")
    client = Client.objects.get(name="Coca-Cola")
    first_names = _get_first_names()
    for nationality in all_countries:
        try:
            last_name = first_names[nationality.name[0].lower()]
        except KeyError:
            print(f"No name found for {nationality}", file=sys.stderr)
        else:
            print(f"{nationality} {last_name}")
        email = _make_email(f"{nationality}-{last_name}", client.entity_domain_name)
        user = _create_user(
            first_name=nationality.name, last_name=last_name, email=email
        )
        applicant = Applicant.objects.create(
            employer=client,
            home_country_uuid=belgium.uuid,
            user_uuid=user.uuid,
        )
        ApplicantNationality.objects.create(
            applicant=applicant, country_uuid=nationality.uuid
        )


def _get_first_names():
    from faker.providers.person import en_GB
    from faker.providers.person import de_DE
    from faker.providers.person import fr_FR
    from faker.providers.person import pt_PT

    first_names = set(
        chain.from_iterable(
            loc.Provider.first_names for loc in [en_GB, de_DE, fr_FR, pt_PT]
        )
    )
    return {name[0].lower(): name for name in first_names}


def _create_user(
    first_name: str,
    last_name: str,
    email: str,
) -> User:
    user = get_user_model().objects.create_user(
        username=email,
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=os.environ["OWLDOCK_DEV_PASSWORD"],
    )
    return user


def _make_email(name: str, domain_name: str) -> str:
    domain_name = strip_prefix(domain_name, "www.")
    domain_name = strip_prefix(domain_name, "www2.")
    company = domain_name.split(".")[0].translate({" ": "-", ",": "-"})  # type: ignore
    return f"{name}-{company}@example.com".lower()
