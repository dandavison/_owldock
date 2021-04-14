import pytest

from django.conf import settings

from app.fixtures import country as country_fixture
from app.fixtures import process as process_fixture
from app.models import Process
from app.tests import factories


def pytest_sessionstart(session):
    from django.test import TestCase
    from django.test import TransactionTestCase

    # The usual behavior is for transactions to be rolled back after each test,
    # and that is what we want. However, unless we do the following,
    # transactions will only be rolled back on the default database.
    # https://github.com/pytest-dev/pytest-django/issues/76
    TestCase.databases = TransactionTestCase.databases = set(settings.DATABASES.keys())


@pytest.fixture(autouse=True)
def allow_database_use(db):
    pass


@pytest.fixture()
def load_country_fixture():
    country_fixture.load_country_fixture()


@pytest.fixture()
def load_process_fixture(load_country_fixture):
    process_fixture.load_process_fixture()


@pytest.fixture
def process_A(load_process_fixture):
    return Process.objects.order_by("id")[0]


@pytest.fixture
def process_B(load_process_fixture):
    return Process.objects.order_by("id")[1]


@pytest.fixture
def provider_A():
    return factories.ProviderFactory()


@pytest.fixture
def provider_B():
    return factories.ProviderFactory()


@pytest.fixture
def provider_contact_A(provider_A):
    return factories.ProviderContactFactory(provider=provider_A)


@pytest.fixture
def provider_contact_B(provider_B):
    return factories.ProviderContactFactory(provider=provider_B)
