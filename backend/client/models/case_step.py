import logging
from typing import Callable, List

from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models import deletion, QuerySet
from django.db.transaction import atomic
from django.urls import reverse
from django.utils import timezone

from app.models import ProcessStep, ProviderContact, StoredFile, User
from app.models.file import ApplicationFileType
from client.models.client import Case
from owldock.state_machine.action import Action
from owldock.state_machine.django_fsm_utils import FSMField, transition
from owldock.state_machine.role import get_role, Role
from owldock.models.base import BaseModel
from owldock.models.fields import UUIDPseudoForeignKeyField

logger = logging.getLogger(__file__)


class State(models.TextChoices):
    FREE = "Waiting for user to select a provider"
    EARMARKED = "Waiting for user to notify provider"
    OFFERED = "Waiting for provider to accept"
    # TODO: Introduce concept of step being accepted but not ready to work on
    # (e.g. due to dependencies)
    # ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "In progress"
    COMPLETE = "Complete"


ACTIONS = {
    (Role.CLIENT_CONTACT, State.FREE): [
        ("Save", "client_contact_earmark_case_step"),
    ],
    (Role.CLIENT_CONTACT, State.EARMARKED): [
        ("Save", "client_contact_earmark_case_step"),
        ("Notify Provider", "client_contact_offer_case_step"),
    ],
    (Role.CLIENT_CONTACT, State.OFFERED): [
        ("Retract", "client_contact_retract_case_step"),
    ],
    (Role.PROVIDER_CONTACT, State.OFFERED): [
        ("Accept", "provider_contact_accept_case_step"),
        ("Reject", "provider_contact_reject_case_step"),
    ],
    (Role.CLIENT_CONTACT, State.IN_PROGRESS): [
        ("Retract", "client_contact_retract_case_step"),
    ],
    (Role.PROVIDER_CONTACT, State.IN_PROGRESS): [
        ("Mark completed", "provider_contact_complete_case_step"),
        ("Reject", "provider_contact_reject_case_step"),
    ],
}


def permission_checker(action: str) -> Callable[["CaseStep", User], bool]:
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
            return instance.case.client_contact.user == user  # type: ignore
        elif role == Role.PROVIDER_CONTACT:
            contract = instance.active_contract
            return bool(contract) and contract.provider_contact.user == user  # type: ignore
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
    process_step: ProcessStep
    sequence_number = models.PositiveIntegerField()
    active_contract = models.OneToOneField(
        "CaseStepContract", null=True, on_delete=deletion.SET_NULL
    )
    state_name = FSMField(default=State.FREE.name, protected=True)

    # Added by django-fsm
    get_available_state_name_transitions: Callable
    get_available_user_state_name_transitions: Callable

    def validate(self):
        # TODO: Should UUIDPseudoForeignKeyField cause this to happen
        # automatically?
        assert (
            self.process_step_uuid
            and ProcessStep.objects.filter(uuid=self.process_step_uuid).exists()
        )

    @property
    def state(self) -> State:
        return getattr(State, self.state_name)

    def has_active_contract(self) -> bool:
        return bool(self.active_contract)

    def has_blank_active_contract(self) -> bool:
        if not self.active_contract:
            return False
        return (
            self.active_contract.accepted_at is None
            and self.active_contract.rejected_at is None
        )

    @transition(
        field=state_name,
        source=[State.FREE, State.EARMARKED],
        target=State.EARMARKED,
        conditions=[],  # does_not_have_accepted_contract?
        permission=permission_checker("client_contact_offer_case_step"),
    )
    def earmark(self, provider_contact: ProviderContact) -> None:
        """
        Associate this case with a provider without notifying the provider.
        """
        with atomic():
            contract, created = CaseStepContract.objects.get_or_create(
                case_step=self,
                provider_contact_uuid=provider_contact.uuid,
                accepted_at__isnull=True,
                rejected_at__isnull=True,
            )
            self.active_contract = contract
            self.save()
            logger.info(
                "Earmarked %s for %s (contract was %s)",
                contract,
                provider_contact,
                "new" if created else "pre-existing",
            )

    @transition(
        field=state_name,
        source=State.EARMARKED,
        target=State.OFFERED,
        conditions=[has_blank_active_contract],
        permission=permission_checker("client_contact_offer_case_step"),
    )
    def offer(self, provider_contact: ProviderContact) -> None:
        """
        Offer this case to a provider; they may then accept or reject it.
        """
        from app.outbound_messaging import OfferedCaseStepsNotifier

        OfferedCaseStepsNotifier(provider_contact, [self]).notify()

    @transition(
        field=state_name,
        source=State.OFFERED,
        target=State.IN_PROGRESS,
        conditions=[has_active_contract],
        permission=permission_checker("provider_contact_accept_case_step"),
    )
    def accept(self) -> None:
        assert self.active_contract, "source state implies active contract exists"
        self.active_contract.accepted_at = timezone.now()
        self.active_contract.save()

    @transition(
        field=state_name,
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
        field=state_name,
        source=[State.OFFERED, State.IN_PROGRESS],
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
            assert active_contract, "source states imply that active contract exists"
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

    def add_uploaded_files(
        self,
        uploaded_files: List[UploadedFile],
        user: User,
        role: Role,
    ) -> None:
        assert get_role(user) == role, "Supplied user doesn't match supplied role"
        application_file_type = {
            Role.CLIENT_CONTACT: ApplicationFileType.CLIENT_CONTACT_UPLOAD,
            Role.PROVIDER_CONTACT: ApplicationFileType.PROVIDER_CONTACT_UPLOAD,
        }[role]
        for uploaded_file in uploaded_files:
            stored_file = StoredFile.from_uploaded_file(uploaded_file)
            stored_file.created_by = user
            stored_file.associated_object_uuid = self.uuid
            stored_file.associated_object_content_type = self.content_type
            stored_file.application_file_type = application_file_type
            stored_file.save()

    @property
    def stored_files(self) -> QuerySet[StoredFile]:
        prefetched = getattr(self, "_prefetched_stored_files", None)
        if prefetched:
            return prefetched

        # GenericRelation is not working with our multiple database setup
        return StoredFile.objects.filter(
            associated_object_uuid=self.uuid,
            associated_object_content_type=self.content_type,
        )


class CaseStepContract(BaseModel):
    case_step = models.ForeignKey(CaseStep, on_delete=deletion.CASCADE)
    provider_contact_uuid = UUIDPseudoForeignKeyField(ProviderContact)
    provider_contact: ProviderContact
    accepted_at = models.DateTimeField(null=True)
    rejected_at = models.DateTimeField(null=True)

    def validate(self):
        # TODO: Should UUIDPseudoForeignKeyField cause this to happen
        # automatically?
        assert (
            self.provider_contact_uuid
            and ProviderContact.objects.filter(uuid=self.provider_contact_uuid).exists()
        )

    def is_blank(self) -> bool:
        return not self.accepted_at and not self.rejected_at
