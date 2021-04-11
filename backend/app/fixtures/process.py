import csv
import re
from typing import List, Tuple

from django.conf import settings


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
