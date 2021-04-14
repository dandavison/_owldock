from typing import Callable, List

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import deletion, Model, QuerySet
from django.db.transaction import atomic
from django.urls import reverse
from django.utils import timezone

from app.models import ProcessStep, ProviderContact, StoredFile, User
from client.models.client import Case
from owldock.state_machine.action import Action
from owldock.state_machine.django_fsm_utils import FSMField, transition
from owldock.state_machine.role import get_role, Role
from owldock.models.base import BaseModel
from owldock.models.fields import UUIDPseudoForeignKeyField


class State(models.TextChoices):
    FREE = "Waiting for client to offer to provider"
    OFFERED = "Waiting for provider to accept"
    # TODO: Introduce concept of step being accepted but not ready to work on
    # (e.g. due to dependencies)
    # ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "In progress"
    COMPLETE = "Complete"


ACTIONS = {
    (Role.CLIENT_CONTACT, State.FREE.name): [
        ("Offer", "client_contact_offer_case_step"),
    ],
    (Role.CLIENT_CONTACT, State.OFFERED.name): [
        ("Retract", "client_contact_retract_case_step"),
    ],
    (Role.PROVIDER_CONTACT, State.OFFERED.name): [
        ("Accept", "provider_contact_accept_case_step"),
        ("Reject", "provider_contact_reject_case_step"),
    ],
    (Role.CLIENT_CONTACT, State.IN_PROGRESS.name): [
        ("Retract", "client_contact_retract_case_step"),
    ],
    (Role.PROVIDER_CONTACT, State.IN_PROGRESS.name): [
        ("Mark completed", "provider_contact_complete_case_step"),
        ("Reject", "provider_contact_reject_case_step"),
    ],
}


def permission_checker(action: str) -> Callable[[Model, User], bool]:
    """
    Return a django-fsm permission-checker function.

    I.e. a function mapping (instance, user) -> bool.
    """

    def checker(instance: "CaseStep", user: User) -> bool:
        assert isinstance(instance, CaseStep)
        roles = {
            role
            for (role, _), actions in ACTIONS.items()
            if action in [a for (_, a) in actions]
        }
        role = get_role(user)
        if role not in roles:
            return False
        if role == Role.CLIENT_CONTACT:
            return instance.case.client_contact.user == user
        elif role == Role.PROVIDER_CONTACT:
            contract = instance.active_contract
            return contract and contract.provider_contact.user == user
        else:
            raise AssertionError(f"Invalid role: {role}")

    return checker


class CaseStep(BaseModel):
    # Case steps are concrete steps attached to a case instance. Typically, they
    # will be in 1-1 correspondence with the abstract case.process.steps.
    # However, it may sometimes be desirable to modify a case's steps so that
    # they no longer exactly match any abstract process's steps.
    case = models.ForeignKey(Case, on_delete=deletion.CASCADE)
    process_step_uuid = UUIDPseudoForeignKeyField(ProcessStep)
    sequence_number = models.PositiveIntegerField()
    active_contract = models.OneToOneField(
        "CaseStepContract", null=True, on_delete=deletion.SET_NULL
    )
    state = FSMField(default=State.FREE.name, protected=True)

    def has_active_contract(self) -> bool:
        return bool(self.active_contract)

    def does_not_have_active_contract(self) -> bool:
        return not self.has_active_contract()

    @transition(
        field=state,
        source=State.FREE,
        target=State.OFFERED,
        conditions=[does_not_have_active_contract],
        permission=permission_checker("client_contact_offer_case_step"),
    )
    def offer(self, provider_contact: ProviderContact) -> None:
        """
        Offer this case to a provider; they may then accept or reject it.

        The case may be offered iff:
        - This client contact has write access to it
        - It is offerable (i.e. the case state machine features a transition
          from its current state to offered)
        """
        with atomic():
            contract = CaseStepContract.objects.create(
                case_step=self, provider_contact_uuid=provider_contact.uuid
            )
            self.active_contract = contract
            self.save()

    @transition(
        field=state,
        source=State.OFFERED,
        target=State.IN_PROGRESS,
        conditions=[has_active_contract],
        permission=permission_checker("provider_contact_accept_case_step"),
    )
    def accept(self) -> None:
        self.active_contract.accepted_at = timezone.now()
        self.active_contract.save()

    @transition(
        field=state,
        source=State.IN_PROGRESS,
        target=State.COMPLETE,
        conditions=[has_active_contract],
        permission=permission_checker("provider_contact_complete_case_step"),
    )
    def complete(self) -> None:
        pass

    # retract (client contact) and reject (provider contact) are the same
    # operation done by users in different roles: they both make it so the case
    # step is no longer offered to the provider contact.
    _reject_or_retract_kwargs = dict(
        field=state,
        source=list(set(State) - {State.FREE}),
        target=State.FREE,
        conditions=[has_active_contract],
    )

    @transition(
        permission=permission_checker("provider_contact_reject_case_step"),
        **_reject_or_retract_kwargs,
    )
    def reject(self) -> None:
        with atomic():
            active_contract = self.active_contract
            active_contract.rejected_at = timezone.now()
            active_contract.save()
            self.active_contract = None
            self.save()

    @transition(
        permission=permission_checker("client_contact_retract_case_step"),
        **_reject_or_retract_kwargs,
    )
    def retract(self) -> None:
        self.reject()

    def get_actions(self, user=None) -> List[Action]:
        # TODO: Better separation of HTTP API from models.py
        # This method is currently implemented here on the model class in order
        # that it is available to a DRF serializer.

        from django_tools.middlewares.ThreadLocal import get_current_user
        from owldock.state_machine.role import get_role

        user = user or get_current_user()
        if not user:
            return []
        role = get_role(user)
        if not role:
            return []

        actions = ACTIONS.get((role, self.state), [])
        ret = [
            Action(
                display_name=display_name,
                name=name,
                url=reverse(name, kwargs={"uuid": self.uuid}),
            )
            for (display_name, name) in actions
        ]
        return ret

    @property
    def stored_files(self) -> QuerySet[StoredFile]:
        # GenericRelation is not working with our multiple database setup
        return StoredFile.objects.filter(
            associated_object_uuid=self.uuid,
            associated_object_content_type=ContentType.objects.get_for_model(CaseStep),
        )


class CaseStepContract(BaseModel):
    case_step = models.ForeignKey(CaseStep, on_delete=deletion.CASCADE)
    provider_contact_uuid = UUIDPseudoForeignKeyField(ProviderContact)
    # TODO: db-level constraint that at most one of these may be non-null
    accepted_at = models.DateTimeField(null=True)
    rejected_at = models.DateTimeField(null=True)
