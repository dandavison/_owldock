from django.conf import settings


def pytest_sessionstart(session):
    from django.test import TestCase
    from django.test import TransactionTestCase

    # The usual behavior is for transactions to be rolled back after each test,
    # and that is what we want. However, unless we do the following,
    # transactions will only be rolled back on the default database.
    # https://github.com/pytest-dev/pytest-django/issues/76
    TestCase.databases = TransactionTestCase.databases = set(settings.DATABASES.keys())
