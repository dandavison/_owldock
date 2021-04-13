from django.core.management.base import BaseCommand

from app.fake.set_provider_routes import set_provider_routes


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        set_provider_routes()