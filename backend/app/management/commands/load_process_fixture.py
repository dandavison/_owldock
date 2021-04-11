from django.core.management.base import BaseCommand

from app.fixtures.process import load_process_fixture


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        load_process_fixture()
