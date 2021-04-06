import logging
from typing import List

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models.query import QuerySet
from django.db.transaction import atomic
from django.utils import timezone

from app.models.base import BaseModel
from app.models.process import Route
from app.models.file import ApplicationFileType, StoredFile


logger = logging.getLogger(__name__)
User = get_user_model()


class CaseNotAvailableToProvider(Exception):
    pass


class Provider(BaseModel):
    name = models.CharField(max_length=128)
    logo_url = models.URLField()
    routes = models.ManyToManyField(Route, related_name="providers")


class ProviderContact(BaseModel):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    provider = models.ForeignKey(
        Provider, on_delete=models.deletion.CASCADE, related_name="contacts"
    )

    @atomic  # TODO: are storage writes rolled back?
    def add_uploaded_files_to_case_step(
        self,
        uploaded_files: List[UploadedFile],
        step_id: int,
    ):
        step = self.case_steps_with_write_permission.get(id=step_id)
        for uploaded_file in uploaded_files:
            stored_file = StoredFile.from_uploaded_file(uploaded_file)
            stored_file.created_by = self.user
            stored_file.associated_object = step
            stored_file.application_file_type = (
                ApplicationFileType.PROVIDER_CONTACT_UPLOAD
            )
            stored_file.save()

    @property
    def cases_with_read_permission(self) -> "QuerySet[Case]":
        from app.models.client import Case

        return Case.objects.filter(steps__provider_contact=self).distinct()

    @property
    def case_steps_with_write_permission(self) -> "QuerySet[CaseStep]":
        """
        Provider contact P may write to CaseStep S if S belongs to a case
        assigned to P.
        """
        from app.models.client import CaseStep

        return CaseStep.objects.filter(provider_contact=self)

    def available_cases(self) -> "QuerySet[Case]":
        """
        Return a queryset of cases that are available for this provider to accept.

        A case C is available to provider contact P if a case contract exists for
        (C, P), and that case contract has been neither accepted nor rejected.
        """
        from app.models.client import Case

        return Case.objects.filter(id__in=self._open_contracts().values("case_id"))

    def assigned_cases(self) -> "QuerySet[Case]":
        """
        Return a queryset of cases that are assigned to this provider to work on.

        A case C is available to provider contact P if a case contract exists for
        (C, P), and that case contract has been neither accepted nor rejected.
        """
        from app.models.client import Case

        return Case.objects.filter(id__in=self._accepted_contracts().values("case_id"))

    @atomic
    def accept_case(self, case: "Case") -> None:
        """
        Accept an offered case, i.e. undertake to do the work.
        """
        contract = self._open_contract(case)
        contract.accepted_at = timezone.now()
        contract.save()

    @atomic
    def reject_case(self, case: "Case") -> None:
        """
        Reject an offered case.
        """
        contract = self._open_contract(case)
        contract.rejected_at = timezone.now()
        contract.save()

    def _open_contract(self, case: "Case") -> "CaseContract":
        """
        Return the unique open contract for `case`.

        A contract is open if it is neither accepted nor rejected.
        """
        from app.models.client import CaseContract

        try:
            return self._open_contracts().get(case_id=case.id)
        except CaseContract.DoesNotExist as exc:
            raise CaseNotAvailableToProvider(
                f"{case} is not available to {self}"
            ) from exc
        except CaseContract.MultipleObjectsReturned as exc:
            msg = f"Multiple contracts exist for {self} and {case}"
            logger.exception(msg)
            raise CaseNotAvailableToProvider(msg) from exc

    def _open_contracts(self) -> "QuerySet[CaseContract]":
        """
        Return all open contracts.
        """
        from app.models.client import CaseContract

        return CaseContract.objects.filter(
            provider_contact_id=self.id,
            accepted_at__isnull=True,
            rejected_at__isnull=True,
        )

    def _accepted_contracts(self) -> "QuerySet[CaseContract]":
        """
        Return all accepted contracts.
        """
        from app.models.client import CaseContract

        return CaseContract.objects.filter(
            provider_contact_id=self.id,
            accepted_at__isnull=False,
            rejected_at__isnull=True,
        )
