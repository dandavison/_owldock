from app.http_api.case_step_utils import perform_case_step_transition
from app.http_api.serializers import CaseSerializer
from app.models import ProviderContact
from client.models import CaseStep, ClientContact, State
from client.tests.fake_create_case import fake_create_case_and_earmark_steps


def test_case_step_lifecycle(
    applicant_A,
    applicant_B,
    client_contact_A,
    client_contact_B,
    process_A,
    process_B,
    provider_contact_A,
    provider_contact_B,
):
    # Earmark
    case = fake_create_case_and_earmark_steps(
        applicant_A, client_contact_A, process_A, provider_contact_A
    )
    for case_step in case.steps[:2]:
        _make_case_step_EARMARKED_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_A,
            provider_contact_B,
        )
        # Offer to provider contact A
        perform_case_step_transition(
            "offer",
            client_contact_A.case_steps(),
            "client_contact_A.case_steps()",
            transition_kwargs={"provider_contact": provider_contact_A},
            query_kwargs={"id": case_step.id},
        )
        _make_case_step_OFFERED_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_A,
            provider_contact_B,
        )
        # Provider contact A retracts
        perform_case_step_transition(
            "retract",
            provider_contact_A.case_steps(),
            "provider_contact_A.case_steps()",
            query_kwargs={"id": case_step.id},
        )
        _make_case_step_FREE_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_A,
            provider_contact_B,
        )
        # Earmark, first to provider contact B, then A, and finally B again.
        for provider_contact in [
            provider_contact_B,
            provider_contact_A,
            provider_contact_B,
        ]:
            perform_case_step_transition(
                "earmark",
                client_contact_A.case_steps(),
                "client_contact_A.case_steps()",
                transition_kwargs={"provider_contact": provider_contact},
                query_kwargs={"id": case_step.id},
            )
        perform_case_step_transition(
            "offer",
            client_contact_A.case_steps(),
            "client_contact_A.case_steps()",
            transition_kwargs={"provider_contact": provider_contact_B},
            query_kwargs={"id": case_step.id},
        )
        _make_case_step_OFFERED_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_B,
            provider_contact_A,
        )
        # Provider contact B rejects
        perform_case_step_transition(
            "reject",
            provider_contact_B.case_steps(),
            "provider_contact_B.case_steps()",
            query_kwargs={"id": case_step.id},
        )
        _make_case_step_FREE_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_B,
            provider_contact_A,
        )
        # Offer it to provider contact B again
        perform_case_step_transition(
            "earmark",
            client_contact_A.case_steps(),
            "client_contact_A.case_steps()",
            transition_kwargs={"provider_contact": provider_contact_B},
            query_kwargs={"id": case_step.id},
        )
        perform_case_step_transition(
            "offer",
            client_contact_A.case_steps(),
            "client_contact_A.case_steps()",
            transition_kwargs={"provider_contact": provider_contact_B},
            query_kwargs={"id": case_step.id},
        )
        _make_case_step_OFFERED_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_B,
            provider_contact_A,
        )
        # Provider contact B accepts
        perform_case_step_transition(
            "accept",
            provider_contact_B.case_steps(),
            "provider_contact_B.case_steps()",
            query_kwargs={"id": case_step.id},
        )
        _make_case_step_IN_PROGRESS_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_B,
            provider_contact_A,
        )
        # Provider contact B completes
        perform_case_step_transition(
            "complete",
            provider_contact_B.case_steps(),
            "provider_contact_B.case_steps()",
            query_kwargs={"id": case_step.id},
        )
        _make_case_step_COMPLETE_assertions(
            case_step,
            client_contact_A,
            client_contact_B,
            provider_contact_B,
            provider_contact_A,
        )


def _make_case_step_FREE_assertions(
    case_step: CaseStep,
    client_contact: ClientContact,
    other_client_contact: ClientContact,
    provider_contact: ProviderContact,
    other_provider_contact: ProviderContact,
):
    case_step = CaseStep.objects.get(id=case_step.id)
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

    for c in [client_contact, other_client_contact]:
        list(CaseSerializer.get_cases_for_client_contact(c))


def _make_case_step_EARMARKED_assertions(
    case_step: CaseStep,
    client_contact: ClientContact,
    other_client_contact: ClientContact,
    provider_contact: ProviderContact,
    other_provider_contact: ProviderContact,
):
    case_step = CaseStep.objects.get(id=case_step.id)
    assert case_step.state == State.EARMARKED.name

    # Only owning client contact can see it
    assert case_step in client_contact.case_steps()
    assert case_step not in other_client_contact.case_steps()

    # There is a blank active contract
    assert case_step.active_contract.is_blank()

    # No provider contact can see it
    assert case_step not in provider_contact.case_steps()
    assert case_step not in other_provider_contact.case_steps()

    transitions = _transitions_by_name(case_step.get_available_state_transitions())
    assert set(transitions) == {"earmark", "offer"}

    # Owning Client contact should be able to do: {earmark, offer}
    client_contact_transitions = _transitions_by_name(
        case_step.get_available_user_state_transitions(client_contact.user)
    )
    assert set(client_contact_transitions) == {"earmark", "offer"}
    other_client_contact_transitions = _transitions_by_name(
        case_step.get_available_user_state_transitions(other_client_contact.user)
    )
    assert not other_client_contact_transitions

    # Provider contacts should be able to do nothing
    provider_contact_transitions = _transitions_by_name(
        case_step.get_available_user_state_transitions(provider_contact.user)
    )
    assert not provider_contact_transitions
    other_provider_contact_transitions = _transitions_by_name(
        case_step.get_available_user_state_transitions(other_provider_contact.user)
    )
    assert not other_provider_contact_transitions

    for c in [client_contact, other_client_contact]:
        list(CaseSerializer.get_cases_for_client_contact(c))


def _make_case_step_OFFERED_assertions(
    case_step: CaseStep,
    client_contact: ClientContact,
    other_client_contact: ClientContact,
    provider_contact: ProviderContact,
    other_provider_contact: ProviderContact,
):
    case_step = CaseStep.objects.get(id=case_step.id)
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

    for c in [client_contact, other_client_contact]:
        list(CaseSerializer.get_cases_for_client_contact(c))


def _make_case_step_IN_PROGRESS_assertions(
    case_step: CaseStep,
    client_contact: ClientContact,
    other_client_contact: ClientContact,
    provider_contact: ProviderContact,
    other_provider_contact: ProviderContact,
):
    case_step = CaseStep.objects.get(id=case_step.id)
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

    for c in [client_contact, other_client_contact]:
        list(CaseSerializer.get_cases_for_client_contact(c))


def _make_case_step_COMPLETE_assertions(
    case_step: CaseStep,
    client_contact: ClientContact,
    other_client_contact: ClientContact,
    provider_contact: ProviderContact,
    other_provider_contact: ProviderContact,
):
    case_step = CaseStep.objects.get(id=case_step.id)
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

    for c in [client_contact, other_client_contact]:
        list(CaseSerializer.get_cases_for_client_contact(c))


def _transitions_by_name(transitions) -> dict:
    grouped = {}
    for t in transitions:
        assert t.name not in grouped, f"{t.name} occurs multiple times in transitions"
        grouped[t.name] = t
    return grouped
