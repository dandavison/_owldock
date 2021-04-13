from django.core.management.base import BaseCommand

from app.fake.create_fake_world import create_fake_world


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("password", type=str)

    def handle(self, *args, **kwargs):
        create_fake_world(kwargs["password"])
