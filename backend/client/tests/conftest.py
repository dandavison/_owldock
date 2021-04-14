import pytest

from client.tests import factories


@pytest.fixture
def applicant_A(load_country_fixture):
    return factories.ApplicantFactory()


@pytest.fixture
def applicant_B(load_country_fixture):
    return factories.ApplicantFactory()


@pytest.fixture
def client_contact_A():
    return factories.ClientContactFactory()


@pytest.fixture
def client_contact_B():
    return factories.ClientContactFactory()
