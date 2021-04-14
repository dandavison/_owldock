import pytest

from client.models.case_step import State
from client.tests.fake_create_case import fake_create_case


@pytest.mark.django_db
def test_creation_by_client_contact(
    applicant_A,
    applicant_B,
    client_contact_A,
    client_contact_B,
    process_A,
    process_B,
    provider_contact_A,
    provider_contact_B,
):
    case = fake_create_case(
        applicant_A, client_contact_A, process_A, provider_contact_A
    )
    for case_step in case.steps:
        assert case_step.state == State.OFFERED.name

        # Only client contact A can see it
        assert case_step in client_contact_A.case_steps()
        assert case_step not in client_contact_B.case_steps()

        # Only provider contact B can see it
        assert case_step in provider_contact_A.case_steps()
        assert case_step not in provider_contact_B.case_steps()

        transitions = {
            t
            for t in case_step.get_all_state_transitions()
            if t.source == case_step.state
        }
        [accept] = [t for t in transitions if t.name == "accept"]
        [reject] = [t for t in transitions if t.name == "reject"]
        [retract] = [t for t in transitions if t.name == "retract"]

        assert set(case_step.get_available_state_transitions()) == {
            retract,
            accept,
            reject,
        }

        # Client contact should be able to do: {retract}
        assert set(
            case_step.get_available_user_state_transitions(client_contact_A.user)
        ) == {retract}

        # Provider contact should be able to do: {accept, reject}
        assert set(
            case_step.get_available_user_state_transitions(provider_contact_A.user)
        ) == {accept, reject}
