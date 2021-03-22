import random
from typing import List
from typing import Set
from typing import Type
from typing import TypeVar

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Model
from django_seed import Seed

from app import models
from app.types import Service
from app.types import Status


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
        self.users = iter(create_users(200))
        self.seeder = Seed.seeder()

    def handle(self, *args, **kwargs):
        self.create_fake_clients(3)
        self.create_fake_client_contacts(10)
        self.create_fake_providers(3)
        self.create_fake_provider_contacts(10)
        self.create_fake_employees(100)
        self.create_fake_activities(3)
        self.create_fake_processes(3)
        self.create_fake_cases(200)
        self.seeder.execute()

    def create_fake_clients(self, n: int):
        self.seeder.add_entity(
            models.Client,
            n,
        )

    def create_fake_client_contacts(self, n: int):
        self.seeder.add_entity(
            models.ClientContact, n, {"user": lambda _: next(self.users)}
        )

    def create_fake_providers(self, n: int):
        self.seeder.add_entity(
            models.Provider,
            n,
        )

    def create_fake_provider_contacts(self, n: int):
        self.seeder.add_entity(
            models.ProviderContact, n, {"user": lambda _: next(self.users)}
        )

    def create_fake_employees(self, n: int):
        self.seeder.add_entity(
            models.Employee,
            n,
            {
                "home_country": lambda _: self.seeder.faker.country(),
                "user": lambda _: next(self.users),
            },
        )

    def create_fake_activities(self, n: int):
        for name in ["Give presentation", "Fix engine", "Training"]:
            models.Activity.objects.create(name=name)

    def create_fake_processes(self, n: int):
        for name in ["Immigration Process A", "Immigration Process B"]:
            models.Process.objects.create(name=name)

    def create_fake_cases(self, n: int):
        processes = list(models.Process.objects.all())
        self.seeder.add_entity(
            models.Case,
            n,
            {
                "status": random_case_status,
                "host_country": lambda _: self.seeder.faker.country(),
                # TODO: Why doesn't it pick a Process automatically?
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
