from django.core.management.base import BaseCommand

from app.fake.create_fake_world import create_fake_world


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        create_fake_world()
