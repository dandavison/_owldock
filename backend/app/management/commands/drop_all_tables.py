import sys

import django.apps
from django.core.management.base import BaseCommand
from django.db import connections, ProgrammingError

from app.fake.create_fake_world import assert_this_is_the_fake_world
from owldock.database_router import is_client_model


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        assert_this_is_the_fake_world()
        for model in django.apps.apps.get_models(include_auto_created=True):
            connection = (
                connections["client"]
                if is_client_model(model)
                else connections["default"]
            )
            print(
                f"Dropping table `{model._meta.db_table}` from database `{connection.alias}`"
            )
            with connection.cursor() as cursor:
                execute(f"DROP TABLE {model._meta.db_table} CASCADE", cursor)
        for alias in ["client", "default"]:
            with connections[alias].cursor() as cursor:
                execute("DROP TABLE django_migrations", cursor)
                execute("DROP SEQUENCE django_migrations_id_seq", cursor)


def execute(sql, cursor):
    try:
        cursor.execute(sql)
    except ProgrammingError as exc:
        print(f"{exc.__class__.__name__}({exc})", file=sys.stderr)
