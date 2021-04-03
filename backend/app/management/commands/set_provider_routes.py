from django.core.management.base import BaseCommand
from django.db.transaction import atomic

from app.models import (
    Provider,
    Route,
)


class Command(BaseCommand):
    @atomic
    def handle(self, *args, **kwargs):
        group_a, group_b = [
            Route.objects.filter(name__lt="Marl"),
            Route.objects.filter(name__gte="Marl"),
        ]

        for (provider_name, route_group) in [
            ("Acme", group_a),
            ("Deloitte", group_b),
            ("Corporate Relocations", group_b),
        ]:

            provider = Provider.objects.get(name=provider_name)
            provider.routes.add(*route_group)
