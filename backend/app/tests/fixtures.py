import pytest

from app.fixtures import country as country_fixture
from app.fixtures import process as process_fixture
from app.models import Process
from app.tests import factories


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
def applicant_A():
    return factories.ApplicantFactory()


@pytest.fixture
def applicant_B():
    return factories.ApplicantFactory()


@pytest.fixture
def client_contact_A():
    return factories.ClientContactFactory()


@pytest.fixture
def client_contact_B():
    return factories.ClientContactFactory()


@pytest.fixture
def provider_contact_A():
    return factories.ProviderContactFactory()


@pytest.fixture
def provider_contact_B():
    return factories.ProviderContactFactory()
