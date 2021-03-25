import csv
import re
import sys
from typing import List, Tuple

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from app.models import Country, Process, ProcessFlow, Service


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(settings.PROJECT_ROOT / "app/fixtures/processes.csv") as fh:
            self._load_processes_fixture(fh)

    @atomic
    def _load_processes_fixture(self, fh):
        reader = csv.DictReader(fh)
        us = Country.objects.get(name="United States of America")
        uk = Country.objects.get(name="United Kingdom")
        for row in reader:
            try:
                host_country = Country.objects.get(name=row["Host Country"])
            except Country.DoesNotExist:
                print(
                    f"Country name from fixture does not exist: {row['Host Country']}",
                    file=sys.stderr,
                )
                continue
            for nationality in [us, uk]:
                processes_string = row[nationality.name]
                if processes_string == "N/A":
                    continue
                # Hack
                # E.g. '1. Entry Visa Approval Application; 2. Consular Visa Application; 3. Work Permit Application; 4. Multiple Entry Work Visa Application; 5. Residence Visa Application [Work Permit (Highly Skilled)]; 1. Entry Visa Approval Application (BSA); 2. Consular Visa Application; 3. Residence Visa Application [Work Visa (BSA/SOFA Contractor)]'
                for process_string in processes_string.split("];"):
                    if not process_string.endswith("]"):
                        process_string += "]"
                    process_string = process_string.strip()
                    process_name, process_steps = _parse_process(process_string)
                    process = Process.objects.create(
                        name=process_name,
                        host_country=host_country,
                    )
                    process_flow = ProcessFlow.objects.create(
                        process=process,
                        nationality=nationality,
                    )
                    for (n, service_name) in process_steps:
                        service, _ = Service.objects.get_or_create(name=service_name)
                        process_flow.steps.create(sequence_number=n, service=service)


def _parse_process(process_string: str) -> Tuple[str, List[Tuple[float, str]]]:
    """
    E.g. '1. Employment Visa Application; 2. FRRO Registration [Employment Visa]'
    """
    match = re.match("^([^]]+) +\[([^]]+)\]$", process_string)
    assert match, f"'{process_string}'"
    steps, process = [s.strip() for s in match.groups()]
    return (process, _parse_steps(steps))


def _parse_steps(steps_string: str) -> List[Tuple[float, str]]:
    """
    E.g. '1. Employment Visa Application; 2. FRRO Registration'
    """
    steps: List[Tuple[float, str]] = []
    for step in steps_string.split(";"):
        n, step = step.split(".")
        steps.append((float(n.strip()), step.strip()))
    return steps
