import pytest

from django.contrib.auth import get_user_model

from app.models import Provider, ProviderContact
from owldock.state_machine.role import get_role, Role


@pytest.mark.django_db
def test_provider_contact_factory(provider_contact_A, provider_contact_B):
    _make_provider_contact_assertions(provider_contact_A)
    _make_provider_contact_assertions(provider_contact_B)
    assert provider_contact_A != provider_contact_B
    assert provider_contact_A.user != provider_contact_B.user


def _make_provider_contact_assertions(provider_contact: ProviderContact) -> None:
    assert get_role(provider_contact.user) is Role.PROVIDER_CONTACT
    assert isinstance(provider_contact.user, get_user_model())
    assert isinstance(provider_contact.provider, Provider)
