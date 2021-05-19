import pytest

from django.conf import settings
from django.contrib.auth import get_user_model

from app.fixtures import country as country_fixture
from app.models import Bloc, Country
from app.tests import factories
from immigration.tests.conftest import *  # noqa
from owldock.tests.constants import TEST_PASSWORD


def pytest_sessionstart(session):
    from django.test import TestCase
    from django.test import TransactionTestCase

    # The usual behavior is for transactions to be rolled back after each test,
    # and that is what we want. However, unless we do the following,
    # transactions will only be rolled back on the default database.
    # https://github.com/pytest-dev/pytest-django/issues/76
    TestCase.databases = TransactionTestCase.databases = set(settings.DATABASES.keys())


@pytest.fixture()
def django_test_client(client):
    # The name `client` has other meanings in this project.
    return client


@pytest.fixture(autouse=True)
def allow_database_use(db):
    pass


@pytest.fixture()
def load_country_fixture():
    country_fixture.load_country_fixture()


@pytest.fixture
def country_A(load_country_fixture):
    return Country.objects.order_by("id")[0]


@pytest.fixture
def country_B(load_country_fixture):
    return Country.objects.order_by("id")[1]


@pytest.fixture
def brazil():
    return Country.objects.get_or_create_from_code("BR")[0]


@pytest.fixture
def france():
    return Country.objects.get_or_create_from_code("FR")[0]


@pytest.fixture
def greece():
    return Country.objects.get_or_create_from_code("GR")[0]


@pytest.fixture
def brazil_bloc(brazil):
    bloc = Bloc.objects.create(name="Brazil Bloc")
    bloc.countries.add(brazil)
    return bloc


@pytest.fixture
def france_bloc(france):
    bloc = Bloc.objects.create(name="France Bloc")
    bloc.countries.add(france)
    return bloc


@pytest.fixture
def activity_A():
    return factories.ActivityFactory()


@pytest.fixture
def activity_B():
    return factories.ActivityFactory()


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


@pytest.fixture
def admin_user():
    return get_user_model().objects.create_user(
        username="superuser",
        email="superuser@owldock.com",
        first_name="Super",
        last_name="User",
        password=TEST_PASSWORD,
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def admin_user_client(django_test_client, admin_user):
    django_test_client.login(username=admin_user.username, password=TEST_PASSWORD)
    return django_test_client
