import pytest

from django.contrib.auth import get_user_model

from app.models import Country
from client.models import Applicant, Client, ClientContact
from owldock.state_machine.role import get_role, Role


@pytest.mark.django_db
def test_applicant_factory(applicant_A, applicant_B):
    _make_applicant_assertions(applicant_A)
    _make_applicant_assertions(applicant_B)
    assert applicant_A != applicant_B
    assert applicant_A.user != applicant_B.user


def _make_applicant_assertions(applicant: Applicant) -> None:
    assert get_role(applicant.user) is None
    assert isinstance(applicant.user, get_user_model())
    assert isinstance(applicant.home_country, Country)


@pytest.mark.django_db
def test_client_contact_factory(client_contact_A, client_contact_B):
    _make_client_contact_assertions(client_contact_A)
    _make_client_contact_assertions(client_contact_B)
    assert client_contact_A != client_contact_B
    assert client_contact_A.user != client_contact_B.user


def _make_client_contact_assertions(client_contact: ClientContact) -> None:
    assert get_role(client_contact.user) is Role.CLIENT_CONTACT
    assert isinstance(client_contact.user, get_user_model())
    assert isinstance(client_contact.client, Client)
