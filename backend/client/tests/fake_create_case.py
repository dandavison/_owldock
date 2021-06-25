from datetime import timedelta
from typing import List, Tuple

from django.utils import timezone

from app import api as app_api
from app.models import ProviderContact
from client import api as client_api
from client.models import Applicant, Case, ClientContact
from client.models.case_step import State as CaseStepState
from immigration import api as immigration_api
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
    api_obj = client_api.models.Case(**post_data)
    orm_obj = client_api.write.case.create_for_client_contact(
        api_obj, client_contact=client_contact
    )
    return orm_obj


def make_post_data_for_client_contact_case_create_endpoint(
    applicant: Applicant,
    process: ProcessRuleSet,
    provider_contact: ProviderContact,
) -> dict:
    """
    Create the POST data that the UI would send when a client contact is
    creating a case.
    """
    applicant_api_obj = client_api.models.Applicant.from_orm(applicant)
    now = timezone.now()
    move_serlzr = client_api.models.Move(
        **{
            "host_country": process.route.host_country,
            "target_entry_date": now.date(),
            "target_exit_date": (now + timedelta(days=500)).date(),
        }
    )
    process_srlzr = immigration_api.models.ProcessRuleSet.from_orm(process)
    provider_contact_api_obj = app_api.models.ProviderContact.from_orm(provider_contact)
    case_steps_srlzrs = _create_case_steps_from_process_steps(
        [
            (immigration_api.models.ProcessStep.from_orm(s), provider_contact_api_obj)
            for s in ProcessStep.objects.filter(
                processrulesetstep__process_ruleset=process
            )
        ]
    )

    return {
        "applicant": applicant_api_obj.dict(),
        "move": move_serlzr.dict(),
        "process": process_srlzr.dict(),
        "steps": [s.dict() for s in case_steps_srlzrs],
        "provider_contact": provider_contact_api_obj.dict(),
    }


def _create_case_steps_from_process_steps(
    process_steps: List[
        Tuple[immigration_api.models.ProcessStep, app_api.models.ProviderContact]
    ],
) -> List[client_api.models.CaseStep]:
    # Creation of case step data from process step data occurs client-side;
    # simulated here for server-side tests.
    case_steps = []
    for i, (process_step, provider_contact) in enumerate(process_steps, 1):
        case_step = client_api.models.CaseStep(
            **{
                "actions": [],
                "active_contract": {
                    "provider_contact": provider_contact.dict(),
                },
                "process_step": process_step.dict(),
                "state": CaseStepState.FREE.value,
                "stored_files": [],
            }
        )
        case_steps.append(case_step)
    return case_steps
