from django.core.management.base import BaseCommand
from pydantic2ts import generate_typescript_defs


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--module", type=str)
        parser.add_argument("--output", type=str)
        parser.add_argument("--json2ts_cmd", type=str)

    def handle(self, *args, **kwargs):
        for k in list(kwargs):
            if k not in {"module", "output", "json2ts_cmd"}:
                kwargs.pop(k)
        generate_typescript_defs(**kwargs)
