import logging
from typing import List, TYPE_CHECKING
from uuid import UUID

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models.query import QuerySet
from django.db.transaction import atomic
from django.utils import timezone

from app.models.process import Route
from owldock.models.base import BaseModel
from owldock.state_machine.role import Role

if TYPE_CHECKING:
    from client.models import Applicant, Case, CaseStep, CaseStepContract

logger = logging.getLogger(__name__)


class CaseNotAvailableToProvider(Exception):
    pass


class Provider(BaseModel):
    name = models.CharField(max_length=128)
    url = models.URLField()
    logo_url = models.URLField()
    routes = models.ManyToManyField(Route, related_name="providers")
    # TODO: Add a database constraint ensuring that
    # primary_contact.provider == self ?
    primary_contact = models.OneToOneField(
        "ProviderContact",
        on_delete=models.deletion.CASCADE,
        related_name="provider_for_which_primary",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("name",), name="provider__name__unique_constraint"
            )
        ]


class ProviderContact(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE
    )
    provider = models.ForeignKey(Provider, on_delete=models.deletion.CASCADE)

    role = Role.PROVIDER_CONTACT

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user",), name="provider_contact__user__unique_constraint"
            )
        ]

    def cases(self) -> "QuerySet[Case]":
        """
        All cases relevant to this provider contact.

        A case C is included in this set iff any of the following are true:

        - C contains a case step for which the active contract is asssigned to
          this provider contact

        TODO: control visibility of case steps to provider contact.
        """
        from client.models import Case

        return Case.objects.filter(id__in=self.case_steps().values("case_id"))

    def case_steps(self) -> "QuerySet[CaseStep]":
        """
        Case steps for which this provider contact has access permission.

        A provider contact has access to a case step if the active contract for
        the step is for the provider, and it is not merely earmarked.
        """
        from client.models.case_step import CaseStep
        from client.models.case_step import State as CaseStepState

        return CaseStep.objects.filter(
            active_contract__provider_contact_uuid=self.uuid
        ).exclude(state_name=CaseStepState.EARMARKED.name)

    def add_uploaded_files_to_case_step(
        self,
        uploaded_files: List[UploadedFile],
        step_uuid: UUID,
    ):
        step = self.case_steps_with_write_permission.get(uuid=step_uuid)
        step.add_uploaded_files(uploaded_files, self.user, self.role)

    def applicants(self) -> "QuerySet[Applicant]":
        """
        Return all applicants associated with any non-rejected contract
        involving this provider contact.
        """
        from client.models import Applicant, Case

        # TODO: inefficient SQL?
        case_ids = self._all_contracts().values("case_step__case_id")
        return Applicant.objects.filter(
            id__in=Case.objects.filter(id__in=case_ids).values("applicant_id")
        )

    @property
    def case_steps_with_write_permission(self) -> "QuerySet[CaseStep]":  # noqa
        """
        Provider contact P may write to CaseStep S if S belongs to a case step
        assigned to P and the contract is accepted.
        """
        from client.models.case_step import CaseStep

        return CaseStep.objects.filter(
            id__in=self._accepted_contracts().values("case_step_id")
        ).distinct()

    @atomic
    def accept_case_step(self, case_step: "CaseStep") -> None:  # noqa
        """
        Accept an offered case step, i.e. undertake to do the work.
        """
        contract = self._get_open_contract(case_step)
        contract.accepted_at = timezone.now()
        contract.save()

    @atomic
    def reject_case_step(self, case_step: "CaseStep") -> None:  # noqa
        """
        Reject an offered case step.
        """
        contract = self._get_open_contract(case_step)
        contract.rejected_at = timezone.now()
        contract.save()

    def _get_open_contract(self, case_step: "CaseStep") -> "CaseStepContract":  # noqa
        """
        Return the unique open contract for `case_step`.

        A contract is open if it is neither accepted nor rejected.
        """
        from client.models.case_step import CaseStepContract

        try:
            return self._open_contracts().get(case_step=case_step)
        except CaseStepContract.DoesNotExist as exc:
            raise CaseNotAvailableToProvider(
                f"{case_step} is not available to {self}"
            ) from exc
        except CaseStepContract.MultipleObjectsReturned as exc:
            msg = f"Multiple contracts exist for {self} and {case_step}"
            logger.exception(msg)
            raise CaseNotAvailableToProvider(msg) from exc

    def _all_contracts(self) -> "QuerySet[CaseStepContract]":  # noqa
        """
        Return all non-rejected contracts, accepted or not.
        """
        from client.models.case_step import CaseStepContract

        return CaseStepContract.objects.filter(
            provider_contact_uuid=self.uuid,
            rejected_at__isnull=True,
        )

    def _open_contracts(self) -> "QuerySet[CaseStepContract]":  # noqa
        """
        Return all open contracts.
        """
        return self._all_contracts().filter(accepted_at__isnull=True)

    def _accepted_contracts(self) -> "QuerySet[CaseStepContract]":  # noqa
        """
        Return all accepted contracts.
        """
        return self._all_contracts().filter(accepted_at__isnull=False)
