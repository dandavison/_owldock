import logging
from datetime import datetime
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

if TYPE_CHECKING:
    from django.db.models.query import QuerySet

from app.types import Country


logger = logging.getLogger(__name__)
User = get_user_model()


class CaseCannotBeOffered(Exception):
    pass


class CaseNotAvailableToProvider(Exception):
    pass


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"  # type: ignore


class Client(BaseModel):
    name = models.CharField(max_length=128)


class ClientContact(BaseModel):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.deletion.CASCADE)

    def employees(self) -> "QuerySet[Employee]":
        # TODO: these are employees for which the client contact has what permissions?
        # TODO: ClientEntity
        return Employee.objects.filter(employer_id=self.client_id)

    def initiate_case(
        self,
        employee_id: int,
        process_id: int,
        host_country: Country,
        target_entry_date: datetime,
    ) -> "Case":
        """
        Create a case associated with this client contact,
        but not yet offered to any provider.
        """
        now = timezone.now()
        return Case.objects.create(
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
        self, case: "Case", provider_contact: "ProviderContact"
    ) -> None:
        """
        Offer this case to a provider; they may then accept or reject it.
        """
        if CaseContract.objects.filter(case_id=case.id, rejected_at=None).exists():
            raise CaseCannotBeOffered(
                f"A non-rejected contract exists for case {case.id}"
            )
        CaseContract.objects.create(case=case, provider_contact_id=provider_contact.id)


class Provider(BaseModel):
    name = models.CharField(max_length=128)


class ProviderContact(BaseModel):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.deletion.CASCADE)

    def available_cases(self) -> "QuerySet[Case]":
        """
        Return a queryset of cases that are available for this provider to accept.

        A case C is available to provider contact P if a case contract exists for
        (C, P), and that case contract has been neither accepted nor rejected.
        """
        return Case.objects.filter(id__in=self._open_contracts().values("case_id"))

    def assigned_cases(self) -> "QuerySet[Case]":
        """
        Return a queryset of cases that are assigned to this provider to work on.

        A case C is available to provider contact P if a case contract exists for
        (C, P), and that case contract has been neither accepted nor rejected.
        """
        return Case.objects.filter(id__in=self._accepted_contracts().values("case_id"))

    def accept_case(self, case: "Case") -> None:
        """
        Accept an offered case, i.e. undertake to do the work.
        """
        contract = self._open_contract(case)
        contract.accepted_at = timezone.now()
        contract.save()

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
        return CaseContract.objects.filter(
            provider_contact_id=self.id,
            accepted_at__isnull=True,
            rejected_at__isnull=True,
        )

    def _accepted_contracts(self) -> "QuerySet[CaseContract]":
        """
        Return all accepted contracts.
        """
        return CaseContract.objects.filter(
            provider_contact_id=self.id,
            accepted_at__isnull=False,
            rejected_at__isnull=True,
        )


class Employee(BaseModel):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    employer = models.ForeignKey(Client, on_delete=models.deletion.CASCADE)
    home_country = models.CharField(max_length=128)


class Activity(BaseModel):
    name = models.CharField(max_length=128)


class Process(BaseModel):
    name = models.CharField(max_length=128)
    activities = models.ManyToManyField(Activity)


class Case(BaseModel):
    # TODO: created_by (ClientContact or User?)

    # A case is initiated by a client_contact and it will usually stay non-null.
    # It may become null if a ClientContact ceases to be employed by a Client.
    client_contact = models.ForeignKey(
        ClientContact, null=True, on_delete=models.deletion.SET_NULL
    )
    # A case is born without a provider_contact; one is assigned later.
    provider_contact = models.ForeignKey(
        ProviderContact, null=True, on_delete=models.deletion.SET_NULL
    )
    # A case is always associated with an employee.
    employee = models.ForeignKey(Employee, on_delete=models.deletion.CASCADE)

    # A case is always associated with a process
    process = models.ForeignKey(Process, on_delete=models.deletion.PROTECT)

    # TODO: what is this?
    service = models.CharField(max_length=128)

    # Case data
    host_country = models.CharField(max_length=128)
    target_entry_date = models.DateField()
    status = models.CharField(max_length=128)

    # TODO: compute
    progress = models.FloatField()


class CaseContract(BaseModel):
    case = models.ForeignKey(Case, on_delete=models.deletion.CASCADE)
    provider_contact = models.ForeignKey(
        ProviderContact, on_delete=models.deletion.CASCADE
    )
    # TODO: db-level constraint that at most one of these may be non-null
    accepted_at = models.DateTimeField(null=True)
    rejected_at = models.DateTimeField(null=True)
