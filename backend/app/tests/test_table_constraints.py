import pytest

from django.db import IntegrityError
from django.db.transaction import atomic


def test_country_table_name_constraint(country_A, country_B):
    country_A.name = country_B.name
    with pytest.raises(IntegrityError):
        country_A.save()


def test_country_table_code_constraint(country_A, country_B):
    country_A.code = country_B.code
    with pytest.raises(IntegrityError):
        country_A.save()


def test_provider_primary_contact_not_null(provider_contact_A, provider_contact_B):
    provider_A = provider_contact_A.provider

    # Check that we cannot set a null primary contact.
    provider_A.primary_contact = None
    with pytest.raises(IntegrityError):
        provider_A.save()


@pytest.mark.skip
@pytest.mark.django_db(transaction=True)
def test_provider_primary_contact_foreign_key_constraint(
    provider_contact_A, provider_contact_B
):
    """
    Every provider must have exactly one primary contact, who must be an employee
    of that provider.
    """
    # ALTER TABLE app_providercontact
    # ADD CONSTRAINT app_providercontact_compound_unique
    # UNIQUE (id, provider_id);

    # ALTER TABLE app_provider
    # ADD CONSTRAINT app_provider_primary_contact_compound_fk
    # FOREIGN KEY (primary_contact_id, id)
    # REFERENCES app_providercontact (id, provider_id)
    # DEFERRABLE INITIALLY DEFERRED;

    provider_A = provider_contact_A.provider
    # Check that we cannot set a contact of B to be A's primary contact.
    provider_A.primary_contact = provider_contact_B
    with pytest.raises(IntegrityError):
        with atomic():
            provider_A.save()
