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
    for case_step in case.steps[:2]:
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

    for case_step in case.steps[:2]:
        perform_case_step_transition(
            "retract",
            client_contact_A.case_steps(),
            "client_contact_A.case_steps()",
            query_kwargs={"id": case_step.id},
        )
        case_step = CaseStep.objects.get(id=case_step.id)

        _make_case_step_FREE_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_A,
            provider_contact_B,
        )


def test_client_contact_accept_case_step(
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

    for case_step in case.steps[:2]:
        perform_case_step_transition(
            "accept",
            client_contact_A.case_steps(),
            "client_contact_A.case_steps()",
            query_kwargs={"id": case_step.id},
        )
        case_step = CaseStep.objects.get(id=case_step.id)

        _make_case_step_IN_PROGRESS_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_A,
            provider_contact_B,
        )


def test_client_contact_complete_case_step(
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

    for case_step in case.steps[:2]:
        perform_case_step_transition(
            "accept",
            client_contact_A.case_steps(),
            "client_contact_A.case_steps()",
            query_kwargs={"id": case_step.id},
        )
        perform_case_step_transition(
            "complete",
            client_contact_A.case_steps(),
            "client_contact_A.case_steps()",
            query_kwargs={"id": case_step.id},
        )
        case_step = CaseStep.objects.get(id=case_step.id)

        _make_case_step_COMPLETE_assertions(
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

    transitions = set(case_step.get_available_state_transitions())
    [earmark] = [t for t in transitions if t.name == "earmark"]
    assert set(transitions) == {earmark}

    # Owning Client contact should be able to do: {earmark}
    client_contact_transitions = case_step.get_available_user_state_transitions(
        client_contact.user
    )
    assert set(client_contact_transitions) == {earmark}
    other_client_contact_transitions = case_step.get_available_user_state_transitions(
        other_client_contact.user
    )
    assert set(other_client_contact_transitions) == set()

    # Provider contacts should be able to do nothing
    provider_contact_transitions = case_step.get_available_user_state_transitions(
        provider_contact.user
    )
    assert set(provider_contact_transitions) == set()
    other_provider_contact_transitions = case_step.get_available_user_state_transitions(
        other_provider_contact.user
    )
    assert set(other_provider_contact_transitions) == set()


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

    transitions = set(case_step.get_available_state_transitions())
    [accept] = [t for t in transitions if t.name == "accept"]
    [reject] = [t for t in transitions if t.name == "reject"]
    [retract] = [t for t in transitions if t.name == "retract"]
    assert set(transitions) == {retract, accept, reject}

    # Owning client contact should be able to do: {retract}
    client_contact_transitions = case_step.get_available_user_state_transitions(
        client_contact.user
    )
    assert set(client_contact_transitions) == {retract}
    other_client_contact_transitions = case_step.get_available_user_state_transitions(
        other_client_contact.user
    )
    assert set(other_client_contact_transitions) == set()

    # Offeree Provider contact should be able to do: {accept, reject}
    provider_contact_transitions = case_step.get_available_user_state_transitions(
        provider_contact.user
    )
    assert set(provider_contact_transitions) == {accept, reject}

    other_provider_contact_transitions = case_step.get_available_user_state_transitions(
        other_provider_contact.user
    )
    assert set(other_provider_contact_transitions) == set()


def _make_case_step_IN_PROGRESS_assertions(
    case_step: CaseStep,
    client_contact: ClientContact,
    other_client_contact: ClientContact,
    provider_contact: ProviderContact,
    other_provider_contact: ProviderContact,
):
    assert case_step.state == State.IN_PROGRESS.name
    # Only owning client contact can see it
    assert case_step in client_contact.case_steps()
    assert case_step not in other_client_contact.case_steps()

    # Only provider contact to whom it is offered can see it
    assert case_step.active_contract.provider_contact == provider_contact
    assert case_step in provider_contact.case_steps()
    assert case_step not in other_provider_contact.case_steps()

    transitions = set(case_step.get_available_state_transitions())
    [reject] = [t for t in transitions if t.name == "reject"]
    [retract] = [t for t in transitions if t.name == "retract"]
    [complete] = [t for t in transitions if t.name == "complete"]
    assert set(transitions) == {retract, reject, complete}, [
        t.name for t in transitions
    ]

    # Owning client contact should be able to do: {retract}
    client_contact_transitions = case_step.get_available_user_state_transitions(
        client_contact.user
    )
    assert set(client_contact_transitions) == {retract}, [
        t.name for t in client_contact_transitions
    ]
    other_client_contact_transitions = case_step.get_available_user_state_transitions(
        other_client_contact.user
    )
    assert set(other_client_contact_transitions) == set(), [
        t.name for t in other_client_contact_transitions
    ]

    # Offeree Provider contact should be able to do: {reject, complete}
    provider_contact_transitions = case_step.get_available_user_state_transitions(
        provider_contact.user
    )
    assert set(provider_contact_transitions) == {reject, complete}, [
        t.name for t in provider_contact_transitions
    ]
    other_provider_contact_transitions = case_step.get_available_user_state_transitions(
        other_provider_contact.user
    )
    assert set(other_provider_contact_transitions) == set(), [
        t.name for t in other_provider_contact_transitions
    ]


def _make_case_step_COMPLETE_assertions(
    case_step: CaseStep,
    client_contact: ClientContact,
    other_client_contact: ClientContact,
    provider_contact: ProviderContact,
    other_provider_contact: ProviderContact,
):
    assert case_step.state == State.COMPLETE.name
    # Only owning client contact can see it
    assert case_step in client_contact.case_steps()
    assert case_step not in other_client_contact.case_steps()

    # Only provider contact to whom it is offered can see it
    assert case_step.active_contract.provider_contact == provider_contact
    assert case_step in provider_contact.case_steps()
    assert case_step not in other_provider_contact.case_steps()

    # There are no available transitions.
    transitions = set(case_step.get_available_state_transitions())
    assert set(transitions) == set(), [t.name for t in transitions]

    # Client contacts should be able to do nothing.
    client_contact_transitions = case_step.get_available_user_state_transitions(
        client_contact.user
    )
    assert set(client_contact_transitions) == set(), [
        t.name for t in client_contact_transitions
    ]
    other_client_contact_transitions = case_step.get_available_user_state_transitions(
        other_client_contact.user
    )
    assert set(other_client_contact_transitions) == set(), [
        t.name for t in other_client_contact_transitions
    ]

    # Provider contacts should be able to do nothing.
    provider_contact_transitions = case_step.get_available_user_state_transitions(
        provider_contact.user
    )
    assert set(provider_contact_transitions) == set(), [
        t.name for t in provider_contact_transitions
    ]
    other_provider_contact_transitions = case_step.get_available_user_state_transitions(
        other_provider_contact.user
    )
    assert set(other_provider_contact_transitions) == set(), [
        t.name for t in other_provider_contact_transitions
    ]
