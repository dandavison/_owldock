from django.core.management.base import BaseCommand

from app.models import Country
from immigration.data.load_europe_services import load_europe_services
from immigration.models import ProcessRuleSet, ProcessStep, Route, ServiceItem


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        load_europe_services(
            Country,
            ProcessRuleSet,
            ProcessStep,
            Route,
            ServiceItem,
        )
