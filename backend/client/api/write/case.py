from django.db.transaction import atomic

from app import models as app_orm_models
from client import api as client_api
from client import models as client_orm_models
from immigration import models as immigration_orm_models


@atomic
def create_for_client_contact(
    api_case_instance: client_api.models.Case,
    client_contact: client_orm_models.ClientContact,
) -> client_orm_models.Case:
    api_case_data = api_case_instance.dict()
    applicant_data = api_case_data.pop("applicant")
    move_data = api_case_data.pop("move")
    process_data = api_case_data.pop("process")
    case_steps_data = api_case_data.pop("steps")

    case = client_orm_models.Case.objects.create(
        client_contact=client_contact,
        applicant=client_orm_models.Applicant.objects.get(uuid=applicant_data["uuid"]),
        process_uuid=process_data["uuid"],
        target_entry_date=move_data["target_entry_date"],
        target_exit_date=move_data["target_exit_date"],
    )

    for case_step_data in case_steps_data:
        case_step = case.steps.create(
            process_step_uuid=case_step_data["process_step"]["uuid"],
        )
        provider_contact = app_orm_models.ProviderContact.objects.get(
            uuid=case_step_data["active_contract"]["provider_contact"]["uuid"]
        )
        case_step.earmark(provider_contact)
        case_step.save()

    return case
