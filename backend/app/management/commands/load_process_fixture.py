import sys

from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from app.models import Country, Route, Process, Service
from app.fixtures.process import read_process_fixture


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self._load_process_fixture()

    @atomic
    def _load_process_fixture(self):
        for (
            host_country_name,
            process_name,
            nationality_name,
            process_steps,
        ) in read_process_fixture():
            try:
                host_country = Country.objects.get(name=host_country_name)
            except Country.DoesNotExist:
                print(
                    f"Country name from fixture does not exist: {host_country_name}",
                    file=sys.stderr,
                )
                continue
            route = Route.objects.create(
                name=process_name,
                host_country=host_country,
            )
            process = Process.objects.create(
                route=route,
                nationality=Country.objects.get(name=nationality_name),
            )
            for (n, service_name) in process_steps:
                service, _ = Service.objects.get_or_create(name=service_name)
                process.steps.create(sequence_number=n, service=service)
