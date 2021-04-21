from django.core.management.base import BaseCommand

from app.fake.create_fake_cases import create_fake_cases


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        create_fake_cases(100)
