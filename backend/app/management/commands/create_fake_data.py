import random
from typing import List

from django.core.management.base import BaseCommand
from django_seed import Seed

from app.models import Employee
from app.models import Case
from app.types import CaseType
from app.types import Service
from app.types import Status


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
        self.seeder = Seed.seeder()

    def handle(self, *args, **kwargs):
        self.create_fake_employees(100)
        self.create_fake_cases(200)
        self.seeder.execute()

    def create_fake_employees(self, n_employees: int):
        self.seeder.add_entity(
            Employee,
            n_employees,
            {"home_country": lambda _: self.seeder.faker.country()},
        )

    def create_fake_cases(self, n_cases: int):
        self.seeder.add_entity(
            Case,
            n_cases,
            {
                "case_type": random_case_type,
                "current_status": random_status,
                "host_country": lambda _: self.seeder.faker.country(),
                "progress": lambda _: random.randint(0, 100),
                "service": random_service,
            },
        )


def random_case_type(_) -> List[CaseType]:
    return random.sample({"Case Type A", "Case Type B"}, 1)[0]


def random_status(_) -> List[Status]:
    return random.sample({"Application Submitted", "Application Approved", "Complete"}, 1)[0]


def random_service(_) -> List[Service]:
    return random.sample({"Immigration"}, 1)[0]
