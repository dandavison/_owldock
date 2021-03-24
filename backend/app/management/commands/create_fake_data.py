import random
from typing import List, Set, Type, TypeVar, Optional

from app import models
from app.constants import GroupName
from app.types import Service, Status
import django_countries
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.db.models import Model
from django.db.transaction import atomic
from django_seed import Seed


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("password", type=str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.seeder = Seed.seeder()

    @atomic
    def handle(self, *args, **kwargs):
        self.password = kwargs["password"]
        self._create_superusers()
        self._create_client_contacts()
        self._create_provider_contacts()
        self._create_employees(10)
        self._create_activities(3)
        self._create_processes(3)

    def _create_superusers(self) -> None:
        for (email, first_name, last_name) in [
            ("dandavison7@gmail.com", "Dan", "Davison"),
            ("maria.kouri@corporaterelocations.gr", "Maria", "Kouri"),
            ("sophy@owlimmigration.com", "Sophy", "King"),
        ]:
            User.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=self.password,
                is_staff=True,
                is_superuser=True,
            )

    def _create_client_contacts(self) -> None:
        group = Group.objects.create(name=GroupName.CLIENT_CONTACTS.value)
        for (first_name, last_name, client_name, client_entity_domain_name) in [
            ("Carlos", "Carlero", "Coca-Cola", "cocacola.com"),
            ("Petra", "Petrasson", "Pepsi", "pepsi.com"),
        ]:
            email = _make_email(first_name, client_entity_domain_name)
            user = self._create_user(first_name, last_name, email, group)
            client, _ = models.Client.objects.get_or_create(
                name=client_name, entity_domain_name=client_entity_domain_name
            )
            models.ClientContact.objects.create(client=client, user=user)

    def _create_employees(self, n: int) -> None:
        countries = list(django_countries.countries)
        for client in models.Client.objects.all():
            seen: Set[str] = set()
            done = 0
            while done < n:
                first_name, *last_names = self.seeder.faker.name().split()

                if first_name in seen:
                    continue
                seen.add(first_name)
                done += 1

                last_name = " ".join(last_names)
                email = _make_email(first_name, client.entity_domain_name)
                user = self._create_user(first_name, last_name, email, None)
                models.Employee.objects.create(
                    employer=client,
                    user=user,
                    home_country=random.sample(countries, 1)[0],
                )

    def _create_provider_contacts(self) -> None:
        group = Group.objects.create(name=GroupName.PROVIDER_CONTACTS.value)
        for (first_name, last_name, provider_name, client_entity_domain_name) in [
            ("Alice", "Alisson", "Acme", "acme.com"),
            (
                "Cuthbert",
                "Cuthbertson",
                "Corporate Relocations",
                "corporaterelocations.gr",
            ),
            ("Dimitri", "Dimitros", "Deloitte", "deloitte.com"),
        ]:
            email = _make_email(first_name, client_entity_domain_name)
            user = self._create_user(first_name, last_name, email, group)
            provider, _ = models.Provider.objects.get_or_create(name=provider_name)
            models.ProviderContact.objects.create(provider=provider, user=user)

    def _create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        group: Optional[Group],
    ) -> User:
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=self.password,
        )
        if group:
            user.groups.add(group)
        return user

    def _create_activities(self, n: int):
        for name in ["Give presentation", "Fix engine", "Training"]:
            models.Activity.objects.create(name=name)

    def _create_processes(self, n: int):
        for name in ["Immigration Process A", "Immigration Process B"]:
            models.Process.objects.create(name=name)


M = TypeVar("M", bound=Model)


def _random_case_status(_) -> Status:
    statuses = [
        Status("Application Submitted"),
        Status("Application Approved"),
        Status("Complete"),
    ]
    return random.sample(statuses, 1)[0]


def _random_service(_) -> Service:
    services = [Service("Immigration")]
    return random.sample(services, 1)[0]


def _make_email(name: str, entity_domain_name: str) -> str:
    return f"{name.lower()}@{entity_domain_name}"