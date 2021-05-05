from django.core.management.base import BaseCommand
from django_typomatic import generate_ts


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("context", type=str)
        parser.add_argument("output_file", type=str)

    def handle(self, *args, **kwargs):
        generate_ts(kwargs["output_file"], context=kwargs["context"])
