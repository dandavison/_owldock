from typing import Type

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Model

# TODO: should only be imported at type check time but TYPE_CHECKING didn't seem
# to work
from immigration.models import ProcessStep


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        datamigration_process_steps(apps, None)


def datamigration_process_steps(apps, _schema_editor):
    Country = apps.get_model("app", "Country")
    ProcessRuleSetStep = apps.get_model("immigration", "ProcessRuleSetStep")
    ProcessStep = apps.get_model("immigration", "ProcessStep")
    IssuedDocument = apps.get_model("immigration", "IssuedDocument")
    for host_country in Country.objects.all():
        for route in host_country.routes_for_which_host_country.all():
            for process_ruleset in route.processruleset_set.all():
                for process_step in process_ruleset.processstep_set.all():
                    # We must now find the canonical process step matching this one.
                    try:
                        canonical_process_step = host_country.processstep_set.get(
                            name=process_step.name
                        )
                    except ProcessStep.DoesNotExist:
                        # This is the first time we've seen one with this (name, country)
                        canonical_process_step = process_step
                        canonical_process_step.host_country = host_country
                        process_step.save()
                    else:
                        if are_identical(
                            process_step, canonical_process_step, IssuedDocument
                        ):
                            process_step.delete()
                        else:
                            continue

                    # Create an entry linking to the canonical process step,
                    # with this one's sequence number.
                    ProcessRuleSetStep.objects.create(
                        process_ruleset=process_ruleset,
                        process_step=canonical_process_step,
                        sequence_number=process_step.sequence_number,
                    )


def are_identical(
    process_step_A: ProcessStep,
    process_step_B: ProcessStep,
    IssuedDocument: Type[Model],
) -> bool:
    data_A, data_B = [
        canonical_data(s, IssuedDocument) for s in (process_step_A, process_step_B)
    ]
    for k in data_A.keys() | data_B.keys():
        if data_A[k] != data_B[k]:
            print("Process steps with same name do not match:")
            print(
                process_step_A,
                process_step_B,
                k,
                data_A[k],
                data_B[k],
            )
            return False
    return data_A == data_B


def canonical_data(process_step: ProcessStep, IssuedDocument: Type[Model]) -> dict:
    keys = [
        "name",
        "government_fee",
        "estimated_min_duration_days",
        "estimated_max_duration_days",
        "applicant_can_enter_host_country_after",
        "applicant_can_work_in_host_country_after",
        "required_only_if_payroll_location",
        "required_only_if_duration_exceeds",
    ]
    data = {key: getattr(process_step, key) for key in keys}
    data["issued_documents"] = {
        (
            d.issued_document_type.id,
            d.proves_right_to_enter,
            d.proves_right_to_reside,
            d.proves_right_to_work,
        )
        for d in IssuedDocument.objects.filter(process_step=process_step)
    }
    data["serviceitem"] = process_step.serviceitem.description
    return data
