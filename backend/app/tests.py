from datetime import datetime
from datetime import timedelta

from django.core.management import call_command

import pytest

from . import api
from . import models


@pytest.mark.django_db
def test_client_provider_case_lifecycle():
    _setup()

    clientc = api.ClientContact_.objects.earliest("id")
    employee = clientc.client.employee_set.earliest("id")
    process = models.Process.objects.earliest("id")
    providerc_a, providerc_b = api.ProviderContact_.objects.all()[:2]

    # Client contact creates a case
    case = clientc.initiate_case(
        employee_id=employee.id,
        process_id=process.id,
        host_country="Mozambique",
        target_entry_date=datetime.now() + timedelta(weeks=6),
    )
    assert case.provider_contact is None

    # Neither provider can see the case because the client contact hasn't offered it to them.
    for provider in [providerc_a, providerc_b]:
        assert not provider.list_available_cases().filter(id=case.id).exists()

    # Client contact offers the case to provider contact A
    clientc.offer_case_to_provider(providerc_a)

    # The client contact can't offer it again to anyone (provider contact A
    # has exclusive rights to accept the offer).
    with pytest.raises(models.Case.DoesNotExist):
        clientc.offer_case_to_provider(providerc_a)
    with pytest.raises(models.Case.DoesNotExist):
        clientc.offer_case_to_provider(providerc_b)

    # The case still has no provider because it hasn't been accepted
    assert case.provider_contact is None

    # The provider to whom it was offered can see it; the other can't.
    assert providerc_a.list_available_cases().filter(id=case.id).exists()
    assert not providerc_b.list_available_cases().filter(id=case.id).exists()

    # Provider B can't reject the case; it hasn't been offered to them.
    with pytest.raises(models.Case.DoesNotExist):
        providerc_b.reject_case(case)

    # Provider A rejects the case
    providerc_b.reject_case(case)

    # The case still has no provider because it hasn't been accepted
    assert case.provider_contact is None

    # Once again, neither provider can see the case because the client contact
    # hasn't offered it to them.
    for provider in [providerc_a, providerc_b]:
        assert not provider.list_available_cases().filter(id=case.id).exists()

    # Client contact offers the case to provider contact B
    clientc.offer_case_to_provider(providerc_b)

    # The provider to whom it was offered can see it; the other can't.
    assert providerc_b.list_available_cases().filter(id=case.id).exists()
    assert not providerc_a.list_available_cases().filter(id=case.id).exists()

    # Provider B accepts the case
    providerc_b.accept_case(case)

    # The client contact can't offer it again to anyone (it has been accepted)
    with pytest.raises(models.Case.DoesNotExist):
        clientc.offer_case_to_provider(providerc_a)
    with pytest.raises(models.Case.DoesNotExist):
        clientc.offer_case_to_provider(providerc_b)

    # It's no longer in provider B's available cases but is in in their assigned cases.
    assert not providerc_b.list_available_cases().filter(id=case.id).exists()
    assert providerc_b.list_assigned_cases().filter(id=case.id).exists()


def _setup():
    call_command("create_fake_data")
