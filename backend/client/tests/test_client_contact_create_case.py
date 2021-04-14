import pytest

from app.fake.create_fake_world import create_fake_world
from app.models import Process, ProviderContact
from client.models import ClientContact
from client.models.case_step import State as CaseStepState
from client.tests.fake_create_case import fake_create_case


@pytest.mark.django_db
def test_client_provider_case_lifecycle():
    create_fake_world("password")

    client_contact = ClientContact.objects.earliest("id")
    applicant = client_contact.client.applicant_set.earliest("id")
    process = Process.objects.earliest("id")
    provider_contact = ProviderContact.objects.earliest("id")
    case = fake_create_case(applicant, client_contact, process, provider_contact)
    assert case.casestep_set.exists()

    # All case steps are in OFFERED state
    for case_step in case.casestep_set.all():
        assert case_step.active_contract.provider_contact == provider_contact
        assert case_step.state == CaseStepState.OFFERED.name

    # All case steps are in provider contact's offered list
