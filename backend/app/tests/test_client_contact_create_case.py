from datetime import datetime, timedelta
from typing import List, Tuple

import pytest
from django.core.management import call_command

from app.http_api.serializers import (
    ApplicantSerializer,
    CaseSerializer,
    CaseStepSerializer,
    ProcessSerializer,
    ProcessStepSerializer,
    ProviderContactSerializer,
)
from app.models import (
    Process,
    ProviderContact,
)
from client.models import (
    Applicant,
    ClientContact,
)
from client.models.case_step import State as CaseStepState


def _make_post_data_for_client_contact_case_create_endpoint(
    applicant: Applicant,
    provider_contact: ProviderContact,
    process: Process,
) -> dict:
    """
    Create the POST data that the JS client would send when a client contact is
    creating a case.
    """
    applicant_srlzr = ApplicantSerializer(applicant)
    provider_contact_srlzr = ProviderContactSerializer(provider_contact)
    process_srlzr = ProcessSerializer(process)
    case_steps_srlzrs = _create_case_steps_from_process_steps(
        [
            (ProcessStepSerializer(s), provider_contact_srlzr)
            for s in process.steps.all()
        ]
    )

    now = datetime.now()
    return {
        "applicant": applicant_srlzr.data,
        "provider_contact": provider_contact_srlzr.data,
        "process": process_srlzr.data,
        "steps": [s.data for s in case_steps_srlzrs],
        "target_entry_date": now.date(),
        "target_exit_date": (now + timedelta(days=500)).date(),
    }


def _create_case_steps_from_process_steps(
    process_steps: List[Tuple[ProcessStepSerializer, ProviderContactSerializer]],
) -> List[CaseStepSerializer]:
    # Creation of case step data from process step data occurs client-side;
    # simulated here for server-side tests.
    case_steps = []
    for i, (process_step, provider_contact) in enumerate(process_steps, 1):
        case_step = CaseStepSerializer(
            data={
                "process_step": process_step.data,
                "provider_contact": provider_contact.data,
                "sequence_number": i,
                "stored_files": [],
            }
        )
        assert case_step.is_valid(), case_step.errors
        case_steps.append(case_step)
    return case_steps


@pytest.mark.django_db
def test_client_provider_case_lifecycle():
    _setup()

    client_contact = ClientContact.objects.earliest("id")
    applicant = client_contact.client.applicant_set.earliest("id")
    process = Process.objects.earliest("id")
    provider_contact = ProviderContact.objects.earliest("id")

    post_data = _make_post_data_for_client_contact_case_create_endpoint(
        applicant,
        provider_contact,
        process,
    )
    case_serializer = CaseSerializer(data=post_data)
    assert case_serializer.is_valid(), case_serializer.errors
    case = case_serializer.create_for_client_contact(client_contact=client_contact)
    assert case.casestep_set.exists()
    for case_step in case.casestep_set.all():
        assert case_step.active_contract.provider_contact == provider_contact
        assert case_step.state == CaseStepState.OFFERED


def _setup():
    call_command("create_fake_data", "test-password")
