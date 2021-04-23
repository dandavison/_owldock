import csv
import logging
import re
from typing import List, Tuple

from django.conf import settings
from django.db.transaction import atomic

from app.models import Country, Route, Process, Service


logger = logging.getLogger(__file__)


@atomic
def load_process_fixture():
    print("Loading processes")
    for (
        host_country_name,
        process_name,
        nationality_name,
        process_steps,
    ) in read_process_fixture():
        try:
            host_country = Country.objects.get(name=host_country_name)
        except Country.DoesNotExist:
            logger.warning(
                f"Country name from fixture does not exist: {host_country_name}"
            )
            continue
        route, _ = Route.objects.get_or_create(
            name=process_name,
            host_country=host_country,
        )
        process = Process.objects.create(
            route=route,
            nationality=Country.objects.get(name=nationality_name),
        )
        seen = set()
        for (n, service_name) in process_steps:
            if service_name in seen:
                msg = (
                    f"Duplicate service name ({service_name}) "
                    f"for {host_country_name} {process_name}"
                )
                logger.error(msg)
                continue
            else:
                seen.add(service_name)
            service, _ = Service.objects.get_or_create(name=service_name)
            process.steps.create(sequence_number=n, service=service)


def read_process_fixture():
    with open(settings.BASE_DIR / "app/fixtures/process.csv") as fh:
        reader = csv.DictReader(fh)
        us_name = "United States of America"
        uk_name = "United Kingdom"
        for row in reader:
            host_country_name = row["Host Country"]
            for nationality_name in [us_name, uk_name]:
                processes_string = row[nationality_name]
                if processes_string == "N/A":
                    continue
                # Hack
                # E.g. '1. Entry Visa Approval Application; \
                #       2. Consular Visa Application; \
                #       3. Work Permit Application; \
                #       4. Multiple Entry Work Visa Application; \
                #       5. Residence Visa Application
                #       [Work Permit (Highly Skilled)]; \
                #       1. Entry Visa Approval Application (BSA); \
                #       2. Consular Visa Application; \
                #       3. Residence Visa Application \
                #       [Work Visa (BSA/SOFA Contractor)]'
                for process_string in processes_string.split("];"):
                    if not process_string.endswith("]"):
                        process_string += "]"
                    process_string = process_string.strip()
                    process_name, process_steps = _parse_process(process_string)
                    yield host_country_name, process_name, nationality_name, process_steps


def _parse_process(process_string: str) -> Tuple[str, List[Tuple[float, str]]]:
    """
    E.g. '1. Employment Visa Application; 2. FRRO Registration [Employment Visa]'
    """
    match = re.match(r"^([^]]+) +\[([^]]+)\]$", process_string)
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
