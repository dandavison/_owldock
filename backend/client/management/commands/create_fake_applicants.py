from django.core.management.base import BaseCommand

from client.fake.create_fake_applicants import create_fake_applicants


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        create_fake_applicants()
