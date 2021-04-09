import django_fsm


FSMField = django_fsm.FSMField

can_proceed = django_fsm.can_proceed


def transition(**kwargs):
    """
    Wrapper converting enum state values to strings.

    TODO: FSMField does not work with enum values.
    """
    source, target = kwargs["source"], kwargs["target"]
    if isinstance(source, (list, tuple)):
        kwargs["source"] = [s.name for s in source]
    else:
        kwargs["source"] = source.name
    kwargs["target"] = target.name
    return django_fsm.transition(**kwargs)


def why_cant_proceed(bound_method) -> str:
    """
    Return a string describing why `can_proceed` returned False.

    It is invalid to call this function if `can_proceed` would return True.
    """
    # Based on can_proceed
    # https://github.com/viewflow/django-fsm/blob/25562ec28b10c2487beab1d4b9e0b042ec3d9d3b/django_fsm/__init__.py#L552  # noqa
    meta = bound_method._django_fsm
    im_self = getattr(bound_method, "im_self", getattr(bound_method, "__self__"))
    current_state = meta.field.get_state(im_self)

    if not meta.has_transition(current_state):
        return f"{repr(im_self)}.{bound_method.__name__} has no transition from {current_state}"

    # Based on FSMMeta.conditions_met
    # https://github.com/viewflow/django-fsm/blob/25562ec28b10c2487beab1d4b9e0b042ec3d9d3b/django_fsm/__init__.py#L189  # noqa
    transition = meta.get_transition(current_state)

    assert (
        transition is not None
    ), "Transition should exist since has_transition is true."
    assert (
        transition.conditions
    ), "Conditions should exist since calling this function implies that one was not met."
    not_met = [f for f in transition.conditions if not f(im_self)]
    assert not_met
    names = ", ".join(f.__name__ for f in not_met)
    return f"Conditions not met: {names}"
