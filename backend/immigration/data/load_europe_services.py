import json
from typing import Type

from django.conf import settings
from django.db.models import Model
from django.db.transaction import atomic

COUNTRY_NAMES = {"UK": "United Kingdom"}


@atomic
def load_europe_services(
    Country: Type[Model],
    ProcessRuleSet: Type[Model],
    ProcessStep: Type[Model],
    Route: Type[Model],
    ServiceItem: Type[Model],
):
    path = (
        settings.BASE_DIR / "immigration/data/Europe services spreadsheet 05 May.json"
    )
    with open(path) as fp:
        data = json.load(fp)

    for host_country_name, route_data in data.items():
        host_country = Country.objects.get(
            name=COUNTRY_NAMES.get(host_country_name, host_country_name)
        )
        for route_name, service_item_names in route_data.items():
            if route_name == "Ancillary Services":
                continue
            if (
                host_country.name == "United Kingdom"
                and route_name == "Skilled Worker Visa"
            ):
                # Already added to prod DB
                continue
            route = Route.objects.create(name=route_name, host_country=host_country)
            process_rule_set = ProcessRuleSet.objects.create(route=route)
            for service_item_name in service_item_names:
                if service_item_name.lower().startswith("package "):
                    continue
                process_step = ProcessStep.objects.create(
                    process_rule_set=process_rule_set,
                    name=service_item_name[:128],
                )
                ServiceItem.objects.create(
                    process_step=process_step, description=service_item_name
                )
