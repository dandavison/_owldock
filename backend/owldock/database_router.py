from typing import Type

from django.apps import apps
from django.conf import settings
from django.db.models import Model


def _is_client_model(model: Type[Model]) -> bool:
    return model._meta.app_label == settings.CLIENT_DB_NAME


class Router:
    def _route(self, model: Type[Model], **_) -> str:
        return (
            settings.CLIENT_DB_NAME
            if _is_client_model(model)
            else settings.DEFAULT_DB_NAME
        )

    db_for_read = _route
    db_for_write = _route

    def allow_relation(self, obj1: Model, obj2: Model, **_) -> bool:
        """
        A relationship between two tables is allowed only if the two tables are
        in the same database.
        """
        # TODO: Isn't this the behavior that Django gives by default?
        return (
            self.db_for_read(type(obj1))
            == self.db_for_write(type(obj1))
            == self.db_for_read(type(obj2))
            == self.db_for_write(type(obj2))
        )

    def allow_migrate(self, db: str, app_label: str, **_) -> bool:
        """
        A migration operation may execute iff either of the following are true:
        - It's migrating a client model in the client db
        - It's migrating a non-client model in the default db
        """
        assert set(settings.DATABASES) == {"client", "default"}
        assert db in settings.DATABASES
        assert app_label in {m._meta.app_label for m in apps.get_models()}

        return (app_label == "client") == (db == "client")
