import random
from typing import Set, TypeVar, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Model
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
)
from client.models import (
    Client,
    ClientContact,
    ClientProviderRelationship,
    Applicant,
    ApplicantNationality,
)


def create_fake_world(password: str):
    _FakeWorldCreator(password).create()


class _FakeWorldCreator:
    def __init__(self, password):
        self.password = password
        self.seeder = Seed.seeder()

    @atomic
    def create(self):
        load_country_fixture()
        self._create_services()
        self._create_superusers()
        self._create_provider_contacts()
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
            seen: Set[str] = set()
            done = 0
            while done < n:
                *first_names, last_name = self.seeder.faker.name().split()
                first_name = "-".join(first_names).replace(".", "")

                if first_name in seen:
                    continue
                seen.add(first_name)
                done += 1

                email = _make_email(first_name, client.entity_domain_name)
                user = self._create_user(first_name, last_name, email, None)
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

    def _create_provider_contacts(self) -> None:
        print("Creating provider contacts")
        for (
            first_name,
            last_name,
            provider_name,
            client_entity_domain_name,
            logo_url,
        ) in [
            (
                "Archy",
                "Archimedes",
                "Acme",
                "acme.com",
                "https://static.wikia.nocookie.net/warner-bros-entertainment/images/6/6e/Acme-corp.png",  # noqa
            ),
            (
                "Constantin",
                "Carathéodory",
                "Corporate Relocations",
                "corporaterelocations.gr",
                "https://corporaterelocations.gr/wp-content/uploads/2016/01/FAV.png",
            ),
            (
                "Dietrich",
                "Dedekind",
                "Deloitte",
                "deloitte.com",
                "https://upload.wikimedia.org/wikipedia/commons/5/56/Deloitte.svg",
            ),
        ]:
            email = _make_email(first_name, client_entity_domain_name)
            user = self._create_user(first_name, last_name, email)
            provider, _ = Provider.objects.get_or_create(
                name=provider_name, logo_url=logo_url
            )
            ProviderContact.objects.create(provider=provider, user=user)

    def _create_client_contacts(self) -> None:
        print("Creating client contacts")
        for (
            first_name,
            last_name,
            client_name,
            client_entity_domain_name,
            logo_url,
            (preferred_provider, *other_providers),
        ) in [
            (
                "Carlos",
                "Cantor",
                "Coca-Cola",
                "cocacola.com",
                "https://upload.wikimedia.org/wikipedia/commons/c/ce/Coca-Cola_logo.svg",
                ["Corporate Relocations", "Acme"],
            ),
            (
                "Petra",
                "Pythagoras",
                "Pepsi",
                "pepsi.com",
                "https://upload.wikimedia.org/wikipedia/commons/0/0f/Pepsi_logo_2014.svg",
                ["Deloitte", "Acme"],
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
    ) -> settings.AUTH_USER_MODEL:
        user = get_user_model().objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=self.password,
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
                password=self.password,
                is_staff=True,
                is_superuser=True,
            )


M = TypeVar("M", bound=Model)


def _make_email(name: str, entity_domain_name: str) -> str:
    company = entity_domain_name.split(".")[0].translate({" ": "-", ",": "-"})
    return f"{name}-{company}@example.com".lower()
