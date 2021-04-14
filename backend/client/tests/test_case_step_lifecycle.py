from app.models import ProviderContact
from client.models import CaseStep, ClientContact, State
from client.tests.fake_create_case import fake_create_case


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

        _make_case_step_OFFERED_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_A,
            provider_contact_B,
        )


def _make_case_step_OFFERED_assertions(
    case_step: CaseStep,
    client_contact: ClientContact,
    other_client_contact: ClientContact,
    provider_contact: ProviderContact,
    other_provider_contact: ProviderContact,
):
    # Only client contact A can see it
    assert case_step in client_contact.case_steps()
    assert case_step not in other_client_contact.case_steps()

    # Only provider contact B can see it
    assert case_step in provider_contact.case_steps()
    assert case_step not in other_provider_contact.case_steps()

    transitions = {
        t for t in case_step.get_all_state_transitions() if t.source == case_step.state
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
    assert set(case_step.get_available_user_state_transitions(client_contact.user)) == {
        retract
    }

    # Provider contact should be able to do: {accept, reject}
    assert set(
        case_step.get_available_user_state_transitions(provider_contact.user)
    ) == {accept, reject}
