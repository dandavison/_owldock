from app.http_api.serializers import CaseSerializer
from client.models import Case
from client.tests.fake_create_case import (
    make_post_data_for_client_contact_case_create_endpoint,
)


def test_update_case(
    applicant_A,
    applicant_B,
    client_contact_A,
    process_A,
    provider_contact_A,
    provider_contact_B,
):
    # Create
    post_data = make_post_data_for_client_contact_case_create_endpoint(
        applicant_A,
        process_A,
        provider_contact_A,
    )
    case_serializer = CaseSerializer(data=post_data)
    assert case_serializer.is_valid(), case_serializer.errors
    case = case_serializer.create_for_client_contact(client_contact=client_contact_A)

    # Update
    post_data = CaseSerializer(case).data

    # Set new applicant data
    post_data["applicant"]["id"] = applicant_B.id
    # TODO: This isn't necessary, but it's confusing that both UUIDs and IDs are
    # present client-side.
    post_data["applicant"]["uuid"] = applicant_B.uuid

    # Change a provider on a process step
    step = case.casestep_set.get(sequence_number=1 + 1)
    step_data = post_data["steps"][1]
    assert step.active_contract
    assert step.active_contract.provider_contact == provider_contact_A
    step_provider_contact_data = step_data["active_contract"]["provider_contact"]
    assert step_provider_contact_data["uuid"] == str(provider_contact_A.uuid)
    step_provider_contact_data["uuid"] = str(provider_contact_B.uuid)

    case_serializer = CaseSerializer(data=post_data)
    assert case_serializer.is_valid(), case_serializer.errors
    assert case.applicant == applicant_A

    validated_data = case_serializer.validated_data
    assert validated_data.get("uuid"), "Cannot update: no case uuid in POST data"
    uuid = validated_data["uuid"]
    case = Case.objects.prefetch_related("casestep_set").get(uuid=uuid)

    # Actually update
    case_serializer.update(case, validated_data)

    case = Case.objects.get(id=case.id)
    assert case.applicant == applicant_B
    case_step = case.casestep_set.get(sequence_number=1 + 1)
    assert case_step.active_contract
    assert case_step.active_contract.provider_contact == provider_contact_B
