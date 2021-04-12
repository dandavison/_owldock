from datetime import datetime
from typing import Optional

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import deletion, QuerySet
from django.db.transaction import atomic
from django_fsm import FSMField, transition

from app.models.file import StoredFile
from app.models.process import ProcessStep
from app.models.provider import ProviderContact
from client.models import Case
from owldock.models import BaseModel
from owldock.models.fields import UUIDPseudoForeignKeyField


class State(models.TextChoices):
    FREE = "FREE"
    OFFERED = "Waiting for provider to accept"
    # TODO: Introduce concept of step being accepted but not ready to work on
    # (e.g. due to dependencies)
    # ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"


def client_contact_can_offer_case_step(
    case_step: "CaseStep", user: settings.AUTH_USER_MODEL
) -> bool:
    # TODO: Http404
    client_contact = user.clientcontact_set.get()
    return case_step.case.client_contact == client_contact


def _get_active_contract_for_provider_contact(
    case_step: "CaseStep", user: settings.AUTH_USER_MODEL
) -> "Optional[CaseContract]":
    active_contract = case_step.active_contract
    if not active_contract:
        return None
    # TODO: Http404
    provider_contact = user.providercontact_set.get()
    if (
        active_contract.provider_contract_id == provider_contact.id
        and not active_contract.rejected_at
    ):
        return active_contract
    else:
        return None


def provider_contact_can_accept_case_step(
    case_step: "CaseStep", user: settings.AUTH_USER_MODEL
) -> bool:
    active_contract = _get_active_contract_for_provider_contact(case_step, user)
    if not active_contract:
        return False
    return not active_contract.accepted_at


def provider_contact_can_complete_case_step(
    case_step: "CaseStep", user: settings.AUTH_USER_MODEL
) -> bool:
    active_contract = _get_active_contract_for_provider_contact(case_step, user)
    if not active_contract:
        return False
    return active_contract.accepted_at


class CaseStep(BaseModel):
    # Case steps are concrete steps attached to a case instance. Typically, they
    # will be in 1-1 correspondence with the abstract case.process.steps.
    # However, it may sometimes be desirable to modify a case's steps so that
    # they no longer exactly match any abstract process's steps.
    case = models.ForeignKey(Case, on_delete=deletion.CASCADE)
    process_step_id = UUIDPseudoForeignKeyField(ProcessStep)
    sequence_number = models.PositiveIntegerField()
    active_contract = models.OneToOneField(
        "CaseStepContract", null=True, on_delete=deletion.SET_NULL
    )
    state = FSMField(default=State.FREE)

    def has_active_contract(self) -> bool:
        return bool(self.active_contract)

    def does_not_have_active_contract(self) -> bool:
        return not self.has_active_contract()

    @transition(
        field=state,
        source=State.FREE,
        target=State.OFFERED,
        conditions=[does_not_have_active_contract],
        permission=client_contact_can_offer_case_step,
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
                case_step_id=self.id, provider_contact_id=provider_contact.id
            )
            self.active_contract = contract
            self.save()

    @transition(
        field=state,
        source=State.OFFERED,
        target=State.IN_PROGRESS,
        conditions=[has_active_contract],
        permission=provider_contact_can_accept_case_step,
    )
    def accept(self) -> None:
        self.active_contract.accepted_at = datetime.now()
        self.active_contract.save()

    @transition(
        field=state,
        source=State.IN_PROGRESS,
        target=State.COMPLETE,
        conditions=[has_active_contract],
        permission=provider_contact_can_complete_case_step,
    )
    def complete(self) -> None:
        pass

    @transition(
        field=state,
        source=list(set(State) - {State.FREE}),
        target=State.FREE,
        conditions=[has_active_contract],
    )
    def reject(self) -> None:
        with atomic():
            active_contract = self.active_contract
            active_contract.rejected_at = datetime.now()
            active_contract.save()
            self.active_contract = None
            self.save()

    @property
    def stored_files(self) -> QuerySet[StoredFile]:
        # GenericRelation is not working with our multiple database setup
        return StoredFile.objects.filter(
            associated_object_id=self.id,
            associated_object_content_type=ContentType.objects.get_for_model(CaseStep),
        )


class CaseStepContract(BaseModel):
    case_step = models.ForeignKey(CaseStep, on_delete=deletion.CASCADE)
    provider_contact_id = UUIDPseudoForeignKeyField(ProviderContact)
    # TODO: db-level constraint that at most one of these may be non-null
    accepted_at = models.DateTimeField(null=True)
    rejected_at = models.DateTimeField(null=True)
