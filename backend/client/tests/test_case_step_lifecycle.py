from app.http_api.case_step_utils import perform_case_step_transition
from app.models import ProviderContact
from client.models import CaseStep, ClientContact, State
from client.tests.fake_create_case import fake_create_case_and_offer_steps


def test_client_contact_offer_case_step(
    applicant_A,
    applicant_B,
    client_contact_A,
    client_contact_B,
    process_A,
    process_B,
    provider_contact_A,
    provider_contact_B,
):
    case = fake_create_case_and_offer_steps(
        applicant_A, client_contact_A, process_A, provider_contact_A
    )
    for case_step in case.steps:
        _make_case_step_OFFERED_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_A,
            provider_contact_B,
        )


def test_client_contact_retract_case_step(
    applicant_A,
    applicant_B,
    client_contact_A,
    client_contact_B,
    process_A,
    process_B,
    provider_contact_A,
    provider_contact_B,
):
    case = fake_create_case_and_offer_steps(
        applicant_A, client_contact_A, process_A, provider_contact_A
    )

    for case_step in case.steps:
        perform_case_step_transition(
            "retract",
            client_contact_A.case_steps(),
            "client_contact_A.case_steps()",
            id=case_step.id,
        )
        case_step = CaseStep.objects.get(id=case_step.id)

        _make_case_step_FREE_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_A,
            provider_contact_B,
        )


def _make_case_step_FREE_assertions(
    case_step: CaseStep,
    client_contact: ClientContact,
    other_client_contact: ClientContact,
    provider_contact: ProviderContact,
    other_provider_contact: ProviderContact,
):
    assert case_step.state == State.FREE.name

    # Only owning client contact can see it
    assert case_step in client_contact.case_steps()
    assert case_step not in other_client_contact.case_steps()

    # No provider contact can see it
    assert not case_step.active_contract
    assert case_step not in provider_contact.case_steps()
    assert case_step not in other_provider_contact.case_steps()

    transitions = {
        t for t in case_step.get_all_state_transitions() if t.source == case_step.state
    }
    [offer] = [t for t in transitions if t.name == "offer"]

    assert set(case_step.get_available_state_transitions()) == {offer}

    # Owning Client contact should be able to do: {offer}
    assert set(case_step.get_available_user_state_transitions(client_contact.user)) == {
        offer
    }
    assert (
        set(case_step.get_available_user_state_transitions(other_client_contact.user))
        == set()
    )

    # Provider contacts should be able to do nothing
    assert (
        set(case_step.get_available_user_state_transitions(provider_contact.user))
        == set()
    )
    assert (
        set(case_step.get_available_user_state_transitions(other_provider_contact.user))
        == set()
    )


def _make_case_step_OFFERED_assertions(
    case_step: CaseStep,
    client_contact: ClientContact,
    other_client_contact: ClientContact,
    provider_contact: ProviderContact,
    other_provider_contact: ProviderContact,
):
    assert case_step.state == State.OFFERED.name
    # Only owning client contact can see it
    assert case_step in client_contact.case_steps()
    assert case_step not in other_client_contact.case_steps()

    # Only provider contact to whom it is offered can see it
    assert case_step.active_contract.provider_contact == provider_contact
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

    # TODO: If this passes then clean up the above code
    assert set(case_step.get_available_state_transitions()) == transitions

    # Owning client contact should be able to do: {retract}
    assert set(case_step.get_available_user_state_transitions(client_contact.user)) == {
        retract
    }
    assert (
        set(case_step.get_available_user_state_transitions(other_client_contact.user))
        == set()
    )

    # Offeree Provider contact should be able to do: {accept, reject}
    assert set(
        case_step.get_available_user_state_transitions(provider_contact.user)
    ) == {accept, reject}
    assert (
        set(case_step.get_available_user_state_transitions(other_provider_contact.user))
        == set()
    )
