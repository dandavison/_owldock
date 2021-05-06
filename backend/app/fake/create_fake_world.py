import json
import os
import random
from typing import Optional, Tuple
from urllib.parse import urlparse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.transaction import atomic
from django_seed import Seed

from app.fake.set_provider_routes import set_provider_routes
from app.fixtures.country import load_country_fixture
from app.fixtures.process import load_process_fixture
from app.models import (
    Activity,
    Country,
    Provider,
    ProviderContact,
    Service,
    User,
)
from client.models import (
    Client,
    ClientContact,
    ClientProviderRelationship,
    Applicant,
    ApplicantNationality,
)
from owldock.utils import strip_prefix


def create_fake_world():
    _FakeWorldCreator().create()


class _FakeWorldCreator:
    def __init__(self):
        self.seeder = Seed.seeder()

    @atomic
    def create(self):
        load_country_fixture()
        self._create_services()
        self._create_superusers()
        self._create_providers()
        self._create_client_contacts()
        self._create_applicants(10)
        self._create_activities(3)
        load_process_fixture()
        set_provider_routes()

    def _create_services(self) -> None:
        print("Creating services")
        Service.objects.create(name="Complete and submit petition")
        Service.objects.create(name="Book consular appointment")
        Service.objects.create(name="Escort applicant to consular appointment")

    def _create_activities(self, n: int):
        print("Creating activities")
        for name in ["Give presentation", "Fix engine", "Training"]:
            Activity.objects.create(name=name)

    def _create_applicants(self, n: int) -> None:
        print("Creating applicants")
        countries = [
            Country.objects.get(code="GB"),
            Country.objects.get(code="US"),
        ]
        all_countries = list(Country.objects.all())
        for (i, client) in enumerate(Client.objects.all()):
            country = countries[i % len(countries)]
            for _ in range(n):
                user = self._create_fake_user(client.entity_domain_name)

                applicant = Applicant.objects.create(
                    employer=client,
                    home_country_uuid=country.uuid,
                    user_uuid=user.uuid,
                )
                ApplicantNationality.objects.create(
                    applicant=applicant, country_uuid=country.uuid
                )
                is_dual_national = random.uniform(0, 1) < 1 / 3
                if is_dual_national:
                    other_countries = list(set(all_countries) - {country})
                    second_country = random.choice(other_countries)
                    ApplicantNationality.objects.create(
                        applicant=applicant, country_uuid=second_country.uuid
                    )

    def _create_providers(self) -> None:
        print("Creating provider contacts")
        with open(settings.BASE_DIR / "app/fake/providers.json") as fp:
            for provider in json.load(fp):
                self._create_provider(**provider)

    def _create_provider(self, name, url, logo_url) -> None:
        provider = Provider.objects.create(
            name=name,
            logo_url=logo_url,
            url=url,
            # Invalid, but the FK constraint is deferred until the end of
            # the transaction, which allows us to get around the
            # chicken-and-egg problem.
            primary_contact_id=0,
        )
        provider_contacts = [self._create_provider_contact(provider) for _ in range(20)]
        provider.primary_contact = provider_contacts[0]
        provider.save()

    def _create_provider_contact(self, provider) -> ProviderContact:
        domain_name = urlparse(provider.url).netloc
        user = self._create_fake_user(domain_name)
        return ProviderContact.objects.create(provider=provider, user=user)

    def _create_client_contacts(self) -> None:
        print("Creating client contacts")
        for (
            first_name,
            last_name,
            client_name,
            client_entity_domain_name,
            logo_url,
            provider_predicate,
        ) in [
            (
                "Christine",
                "Cantor",
                "Coca-Cola",
                "cocacola.com",
                "https://upload.wikimedia.org/wikipedia/commons/c/ce/Coca-Cola_logo.svg",
                lambda provider: provider.name.lower() < "m",
            ),
            (
                "Petra",
                "Pythagoras",
                "Pepsi",
                "pepsi.com",
                "https://upload.wikimedia.org/wikipedia/commons/0/0f/Pepsi_logo_2014.svg",
                lambda provider: provider.name.lower() >= "m",
            ),
            (
                "FakeFirstName",
                "FakeLastName",
                "FakeClientName",
                "fake-owldock-client.com",
                "https://previews.123rf.com/images/deniaz/deniaz2001/deniaz200100234/138923282-a-logo-design-about-fake-news-fake-news-logo-fake-news-tag-vector-illustration.jpg",  # noqa
                lambda provider: False,
            ),
        ]:
            email = _make_email(first_name, client_entity_domain_name)
            user = self._create_user(first_name, last_name, email)
            client, _ = Client.objects.get_or_create(
                name=client_name,
                entity_domain_name=client_entity_domain_name,
                logo_url=logo_url,
            )
            ClientContact.objects.create(client=client, user_uuid=user.uuid)
            if client_name == "FakeClientName":
                continue
            preferred_provider, *other_providers = [
                p for p in Provider.objects.all() if provider_predicate(p)
            ]

            ClientProviderRelationship.objects.create(
                client=client,
                provider_uuid=Provider.objects.get(name=preferred_provider).uuid,
                preferred=True,
            )
            for provider in other_providers:
                ClientProviderRelationship.objects.create(
                    client=client,
                    provider_uuid=Provider.objects.get(name=provider).uuid,
                    preferred=False,
                )

    def _create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        group: Optional[Group] = None,
    ) -> User:
        user = get_user_model().objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=os.environ["OWLDOCK_DEV_PASSWORD"],
        )
        if group:
            user.groups.add(group)
        return user

    def _create_superusers(self) -> None:
        print("Creating superusers")
        for (email, first_name, last_name) in [
            ("dandavison7@gmail.com", "Dan", "Davison"),
            ("maria.kouri@corporaterelocations.gr", "Maria", "Kouri"),
            ("sophy@owlimmigration.com", "Sophy", "King"),
        ]:
            get_user_model().objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=os.environ["OWLDOCK_DEV_PASSWORD"],
                is_staff=True,
                is_superuser=True,
            )

    def _fake_name(self) -> Tuple[str, str]:
        *first_names, last_name = self.seeder.faker.name().split()
        first_name = "-".join(first_names).replace(".", "")
        return first_name, last_name

    def _create_fake_user(self, domain_name: str):
        while True:
            first_name, last_name = self._fake_name()
            n = random.choice(range(1, 10))
            email = _make_email(f"{first_name}{n}", domain_name)
            if get_user_model().objects.filter(email=email).exists():
                print(".")
            else:
                break
        return self._create_user(first_name, last_name, email)


def _make_email(name: str, domain_name: str) -> str:
    domain_name = strip_prefix(domain_name, "www.")
    domain_name = strip_prefix(domain_name, "www2.")
    company = domain_name.split(".")[0].translate({" ": "-", ",": "-"})  # type: ignore
    return f"{name}-{company}@example.com".lower()


def assert_this_is_the_fake_world():
    assert {c.name for c in Client.objects.all()} == {
        "Coca-Cola",
        "Pepsi",
        "FakeClientName",
    }
    assert {p.name for p in Provider.objects.all()} == {
        "Avocat Grégoire",
        "BLF",
        "Berry Appleman & Leiden",
        "Bretz & Coven",
        "Clark Hill",
        "Corporate Relocations",
        "Cyrus D. Mehta",
        "Deloitte",
        "Deloitte France",
        "Duane Morris",
        "Fragomen",
        "Kramer Levin",
        "Laura Devine",
        "Lexial",
        "Saint Georges Avocats",
    }
