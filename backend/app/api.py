import logging
from datetime import datetime

from django.db.models.query import QuerySet
from django.utils import timezone

from . import models
from .types import Country

logger = logging.getLogger(__name__)


class CaseCannotBeOffered(Exception):
    pass


class CaseNotAvailableToProvider(Exception):
    pass


class ClientContact_(models.ClientContact):
    class Meta:
        proxy = True

    def initiate_case(
        self,
        employee_id: int,
        process_id: int,
        host_country: Country,
        target_entry_date: datetime,
    ) -> models.Case:
        """
        Create a case associated with this client contact,
        but not yet offered to any provider.
        """
        now = timezone.now()
        return models.Case.objects.create(
            created_at=now,
            modified_at=now,
            client_contact=self,
            employee_id=employee_id,
            process_id=process_id,
            host_country=host_country,
            target_entry_date=target_entry_date,
            progress=0.0,
        )

    def offer_case_to_provider(
        self, case: models.Case, provider_contact: models.ProviderContact
    ) -> None:
        """
        Offer this case to a provider; they may then accept or reject it.
        """
        if models.CaseContract.objects.filter(
            case_id=case.id, rejected_at=None
        ).exists():
            raise CaseCannotBeOffered(
                f"A non-rejected contract exists for case {case.id}"
            )
        models.CaseContract.objects.create(
            case=case, provider_contact_id=provider_contact.id
        )


class ProviderContact_(models.Provider):
    class Meta:
        proxy = True

    def available_cases(self) -> QuerySet[models.Case]:
        """
        Return a queryset of cases that are available for this provider to accept.

        A case C is available to provider contact P if a case contract exists for
        (C, P), and that case contract has been neither accepted nor rejected.
        """
        return models.Case.objects.filter(
            id__in=self._open_contracts().values("case_id")
        )

    def assigned_cases(self) -> QuerySet[models.Case]:
        """
        Return a queryset of cases that are assigned to this provider to work on.

        A case C is available to provider contact P if a case contract exists for
        (C, P), and that case contract has been neither accepted nor rejected.
        """
        return models.Case.objects.filter(
            id__in=self._accepted_contracts().values("case_id")
        )

    def accept_case(self, case: models.Case) -> None:
        """
        Accept an offered case, i.e. undertake to do the work.
        """
        contract = self._open_contract(case)
        contract.accepted_at = timezone.now()
        contract.save()

    def reject_case(self, case: models.Case) -> None:
        """
        Reject an offered case.
        """
        contract = self._open_contract(case)
        contract.rejected_at = timezone.now()
        contract.save()

    def _open_contract(self, case: models.Case) -> models.CaseContract:
        """
        Return the unique open contract for `case`.

        A contract is open if it is neither accepted nor rejected.
        """
        try:
            return self._open_contracts().get(case_id=case.id)
        except models.CaseContract.DoesNotExist as exc:
            raise CaseNotAvailableToProvider(
                f"{case} is not available to {self}"
            ) from exc
        except models.CaseContract.MultipleObjectsReturned as exc:
            msg = f"Multiple contracts exist for {self} and {case}"
            logger.exception(msg)
            raise CaseNotAvailableToProvider(msg) from exc

    def _open_contracts(self) -> QuerySet[models.CaseContract]:
        """
        Return all open contracts.
        """
        return models.CaseContract.objects.filter(
            provider_contact_id=self.id,
            accepted_at__isnull=True,
            rejected_at__isnull=True,
        )

    def _accepted_contracts(self) -> QuerySet[models.CaseContract]:
        """
        Return all accepted contracts.
        """
        return models.CaseContract.objects.filter(
            provider_contact_id=self.id,
            accepted_at__isnull=False,
            rejected_at__isnull=True,
        )
