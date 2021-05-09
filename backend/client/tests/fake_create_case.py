from datetime import timedelta
from typing import List, Tuple

from django.utils import timezone

from app.api.serializers import (
    ApplicantSerializer,
    CaseSerializer,
    CaseStepSerializer,
    ProcessSerializer,
    ProcessStepSerializer,
    ProviderContactSerializer,
)
from app.models import ProviderContact
from client.models import Applicant, Case, ClientContact
from client.models.case_step import State as CaseStepState
from immigration.models import ProcessRuleSet, ProcessStep


def fake_create_case_and_earmark_steps(
    applicant: Applicant,
    client_contact: ClientContact,
    process: ProcessRuleSet,
    provider_contact: ProviderContact,
) -> Case:
    post_data = make_post_data_for_client_contact_case_create_endpoint(
        applicant,
        process,
        provider_contact,
    )
    case_serializer = CaseSerializer(data=post_data)
    assert case_serializer.is_valid(), case_serializer.errors
    case = case_serializer.create_for_client_contact(client_contact=client_contact)
    return case


def make_post_data_for_client_contact_case_create_endpoint(
    applicant: Applicant,
    process: ProcessRuleSet,
    provider_contact: ProviderContact,
) -> dict:
    """
    Create the POST data that the UI would send when a client contact is
    creating a case.
    """
    applicant_srlzr = ApplicantSerializer(applicant)
    provider_contact_srlzr = ProviderContactSerializer(provider_contact)
    process_srlzr = ProcessSerializer(process)
    case_steps_srlzrs = _create_case_steps_from_process_steps(
        [
            (ProcessStepSerializer(s), provider_contact_srlzr)
            for s in ProcessStep.objects.filter(
                processrulesetstep__process_ruleset=process
            )
        ]
    )

    now = timezone.now()
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
                "actions": [],
                "active_contract": {
                    "provider_contact": provider_contact.data,
                },
                "process_step": process_step.data,
                "sequence_number": i,
                "state": {
                    "name": CaseStepState.FREE.name,
                    "value": CaseStepState.FREE.value,
                },
                "stored_files": [],
            }
        )
        assert case_step.is_valid(), case_step.errors
        case_steps.append(case_step)
    return case_steps
