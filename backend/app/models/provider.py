import logging
from typing import List
from uuid import UUID

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models.query import QuerySet
from django.db.transaction import atomic
from django.utils import timezone

from app.models.process import Route
from app.models.file import ApplicationFileType, StoredFile
from owldock.models import BaseModel


logger = logging.getLogger(__name__)


class CaseNotAvailableToProvider(Exception):
    pass


class Provider(BaseModel):
    name = models.CharField(max_length=128)
    logo_url = models.URLField()
    routes = models.ManyToManyField(Route, related_name="providers")


class ProviderContact(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.deletion.CASCADE
    )
    provider = models.ForeignKey(Provider, on_delete=models.deletion.CASCADE)

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
        from client.models.case_step import CaseStep

        return CaseStep.objects.filter(active_contract__provider_contact_id=self.id)

    @atomic  # TODO: are storage writes rolled back?
    def add_uploaded_files_to_case_step(
        self,
        uploaded_files: List[UploadedFile],
        step_id: UUID,
    ):
        step = self.case_steps_with_write_permission.get(id=step_id)
        for uploaded_file in uploaded_files:
            stored_file = StoredFile.from_uploaded_file(uploaded_file)
            stored_file.created_by = self.user
            stored_file.associated_object_id = step.id
            stored_file.associated_object_content_type = step.content_type
            stored_file.application_file_type = (
                ApplicationFileType.PROVIDER_CONTACT_UPLOAD
            )
            stored_file.save()

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
    def cases_steps_with_read_permission(self) -> "QuerySet[CaseStep]":  # noqa
        from client.models.case_step import CaseStep

        return CaseStep.objects.filter(
            id__in=self._all_contracts().values("case_step_id")
        ).distinct()

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

    def open_case_steps(self) -> "QuerySet[CaseStep]":  # noqa
        """
        Return a queryset of case steps that are open    for this provider to
        accept.

        A case step S is available to provider contact P if a case step contract
        exists for (S, P), and that contract has been neither accepted nor
        rejected.
        """
        from client.models.case_step import CaseStep

        return CaseStep.objects.filter(
            id__in=self._open_contracts().values("case_step_id")
        ).distinct()

    def assigned_case_steps(self) -> "QuerySet[Case]":  # noqa
        """
        Return a queryset of case steps that are assigned to this provider to
        work on.

        A case step S is assigned to provider contact P if a case step contract
        exists for (S, P), and that case contract has been signed and not
        rejected.
        """
        from client.models.case_step import CaseStep

        return CaseStep.objects.filter(
            id__in=self._accepted_contracts().values("case_step_id")
        )

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
            return self._open_contracts().get(case_step_id=case_step.id)
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
            provider_contact_id=self.id,
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
