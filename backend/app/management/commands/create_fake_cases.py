from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        create_fake_cases(100)
