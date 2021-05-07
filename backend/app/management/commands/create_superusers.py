from django.core.management.base import BaseCommand

from owldock.create_superusers import create_superusers


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        create_superusers()
