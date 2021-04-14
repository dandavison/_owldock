import pytest

from client.tests import factories


@pytest.fixture
def applicant_A(load_country_fixture):
    return factories.ApplicantFactory()


@pytest.fixture
def applicant_B(load_country_fixture):
    return factories.ApplicantFactory()


@pytest.fixture
def client_A():
    return factories.ClientFactory()


@pytest.fixture
def client_B():
    return factories.ClientFactory()


@pytest.fixture
def client_contact_A(client_A):
    return factories.ClientContactFactory(client=client_A)


@pytest.fixture
def client_contact_B(client_B):
    return factories.ClientContactFactory(client=client_B)
