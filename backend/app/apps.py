from django.apps import AppConfig as _AppConfig

from app import signal_receivers  # noqa


class AppConfig(_AppConfig):
    name = "app"
