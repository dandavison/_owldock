from django.core.management.base import BaseCommand

from app.fixtures.country import load_country_fixture


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        load_country_fixture()
