from django.core.management.base import BaseCommand

from immigration.fake.create_fake_process_rulesets import create_fake_process_rulesets


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        create_fake_process_rulesets()
