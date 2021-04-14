import pytest

from django.contrib.auth import get_user_model

from app.models import Provider, ProviderContact
from owldock.state_machine.role import get_role, Role


def test_activity_factory(activity_A, activity_B):
    assert activity_A != activity_B
    assert activity_A.name != activity_B.name


def test_provider_contact_factory(
    provider_A, provider_contact_A, provider_B, provider_contact_B
):
    _make_provider_contact_assertions(provider_A, provider_contact_A)
    _make_provider_contact_assertions(provider_B, provider_contact_B)
    assert provider_A != provider_B
    assert provider_A.name != provider_B.name
    assert provider_contact_A != provider_contact_B
    assert provider_contact_A.user != provider_contact_B.user


def _make_provider_contact_assertions(
    provider: Provider, provider_contact: ProviderContact
) -> None:
    assert provider_contact.provider == provider
    assert get_role(provider_contact.user) is Role.PROVIDER_CONTACT
    assert isinstance(provider_contact.user, get_user_model())
    assert isinstance(provider_contact.provider, Provider)
