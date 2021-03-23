import random
from typing import List, Set, Tuple, Type, TypeVar

from app import models
from app.constants import GroupName
from app.types import Service, Status
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.db.models import Model
from django.db.transaction import atomic
from django_seed import Seed


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("password", type=str)

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
        self.users = iter(create_users(200))
        self.seeder = Seed.seeder()

    @atomic
    def handle(self, *args, **kwargs):
        self.password = kwargs["password"]
        self._create_superusers()
        self._create_client_contacts()
        self._create_provider_contacts()
        self._create_employees(100)
        self._create_activities(3)
        self._create_processes(3)
        self._create_cases(200)
        self.seeder.execute()

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
        for (first_name, last_name, client_name) in [
            ("Alice", "Alisson", "AAA"),
            ("Benoit", "Benoisé", "BBB"),
        ]:
            email = f"{first_name}@{client_name}-client.com".lower()
            user = self._create_user(first_name, last_name, email, group)
            client, _ = models.Client.objects.get_or_create(name=client_name)
            models.ClientContact.objects.create(client=client, user=user)

    def _create_provider_contacts(self) -> None:
        group = Group.objects.create(name=GroupName.PROVIDER_CONTACTS.value)
        for (first_name, last_name, provider_name) in [
            ("Carlos", "Carlero", "CCC"),
            ("Dimitri", "Dimitros", "DDD"),
        ]:
            email = f"{first_name}@{provider_name}-provider.com".lower()
            user = self._create_user(first_name, last_name, email, group)
            provider, _ = models.Provider.objects.get_or_create(name=provider_name)
            models.ProviderContact.objects.create(provider=provider, user=user)

    def _create_user(
        self,
        first_name: str,
        last_name: str,
        email: str,
        group: Group,
    ) -> User:
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=self.password,
        )
        user.groups.add(group)
        return user

    def _create_employees(self, n: int):
        clients = list(models.Client.objects.all())
        self.seeder.add_entity(
            models.Employee,
            n,
            {
                "employer": lambda _: random.sample(clients, 1)[0],
                "home_country": lambda _: self.seeder.faker.country(),
                "user": lambda _: next(self.users),
            },
        )

    def _create_activities(self, n: int):
        for name in ["Give presentation", "Fix engine", "Training"]:
            models.Activity.objects.create(name=name)

    def _create_processes(self, n: int):
        for name in ["Immigration Process A", "Immigration Process B"]:
            models.Process.objects.create(name=name)

    def _create_cases(self, n: int):
        processes = list(models.Process.objects.all())
        client_contacts = list(models.ClientContact.objects.all())
        provider_contacts = list(models.ProviderContact.objects.all())
        self.seeder.add_entity(
            models.Case,
            n,
            {
                "client_contact": lambda _: random.sample(client_contacts, 1)[0],
                "provider_contact": lambda _: random.sample(provider_contacts, 1)[0],
                "status": random_case_status,
                "host_country": lambda _: self.seeder.faker.country(),
                "process": lambda _: random.sample(processes, 1)[0],
                "progress": lambda _: random.randint(0, 100),
                "service": random_service,
            },
        )


def create_users(n: int) -> List[User]:
    seeder = Seed.seeder()
    names: Set[str] = set()
    while len(names) < n:
        names.add(seeder.faker.name())
    users = []
    for name in names:
        email = "-".join(name) + "@example.com"
        first_name, *last_names = name.split()
        last_name = " ".join(last_names)

        users.append(
            User.objects.create(
                email=email, first_name=first_name, last_name=last_name, username=email
            )
        )
    return users


M = TypeVar("M", bound=Model)


def create_entities(model: Type[M], n) -> List[M]:
    seeder = Seed.seeder()
    seeder.add_entity(model, n)
    pks = seeder.execute()[model][:n]
    return list(model.objects.filter(pk__in=pks))


def random_case_status(_) -> Status:
    statuses = [
        Status("Application Submitted"),
        Status("Application Approved"),
        Status("Complete"),
    ]
    return random.sample(statuses, 1)[0]


def random_service(_) -> Service:
    services = [Service("Immigration")]
    return random.sample(services, 1)[0]
