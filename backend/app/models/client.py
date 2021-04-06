import logging
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.query import QuerySet
from django.db.transaction import atomic
from django.utils import timezone

from app.models.base import BaseModel
from app.models.process import Country, Process, ProcessStep
from app.models.provider import Provider, ProviderContact
from app.models.file import StoredFile


logger = logging.getLogger(__name__)
User = get_user_model()


class CaseCannotBeOffered(Exception):
    pass


class Client(BaseModel):
    name = models.CharField(max_length=128)
    entity_domain_name = models.CharField(max_length=128)
    logo_url = models.URLField()
    providers = models.ManyToManyField(
        Provider, through="ClientProviderRelationship", related_name="clients"
    )


class ClientProviderRelationship(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.deletion.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.deletion.CASCADE)
    preferred = models.BooleanField(default=False)

    class Meta:
        unique_together = [["client", "provider"]]
        ordering = ["-preferred"]


class ClientContact(BaseModel):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    client = models.ForeignKey(
        Client, on_delete=models.deletion.CASCADE, related_name="contacts"
    )

    def applicants(self) -> "QuerySet[Applicant]":
        # TODO: these are applicants for which the client contact has what permissions?
        # TODO: ClientEntity
        return Applicant.objects.filter(employer_id=self.client_id)

    def provider_contacts(self, process_id: int) -> QuerySet[ProviderContact]:
        """
        Return provider contacts of client's providers, sorted by preferred
        status with ties broken alphabetically.
        """
        # FIXME: sorting
        providers = self.client.providers.filter(routes__processes=process_id)
        return ProviderContact.objects.filter(provider__in=providers)

    @property
    def cases_with_read_permission(self) -> "QuerySet[Case]":
        return self.case_set.all()

    @atomic
    def initiate_case(
        self,
        applicant_id: int,
        process_id: int,
        target_entry_date: datetime,
        target_exit_date: datetime,
    ) -> "Case":
        """
        Create a case associated with this client contact,
        but not yet offered to any provider.
        """
        now = timezone.now()  # TODO: is this not added automatically?
        return Case.objects.create(
            created_at=now,
            modified_at=now,
            client_contact=self,
            applicant_id=applicant_id,
            process_id=process_id,
            target_entry_date=target_entry_date,
            target_exit_date=target_exit_date,
        )

    @atomic
    def offer_case_to_provider(
        self, case: "Case", provider_contact: "ProviderContact"
    ) -> None:
        """
        Offer this case to a provider; they may then accept or reject it.

        The case may be offered iff:
        - This client contact has write access to it
        - It is offerable (i.e. the case state machine features a transition
          from its current state to offered)
        """
        if not self.has_case_write_permission(case):
            raise CaseCannotBeOffered(
                f"{self} does not have permission to edit {case}."
            )
        if not case.can_be_offered():
            raise CaseCannotBeOffered(f"{case} is not in an offerable state.")
        CaseContract.objects.create(case=case, provider_contact=provider_contact)

    def has_case_write_permission(self, case: "Case") -> bool:
        return case.client_contact == self


class Applicant(BaseModel):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    employer = models.ForeignKey(Client, on_delete=models.deletion.CASCADE)
    home_country = models.ForeignKey(
        Country, on_delete=models.deletion.PROTECT, related_name="applicants_based_in"
    )
    nationalities = models.ManyToManyField(
        Country, related_name="applicants_national_of"
    )


class Case(BaseModel):
    # TODO: created_by (ClientContact or User?)

    # A case is initiated by a client_contact and it will usually stay non-null.
    # It may become null if a ClientContact ceases to be employed by a Client.
    client_contact = models.ForeignKey(
        ClientContact, null=True, on_delete=models.deletion.SET_NULL
    )
    # A case is always associated with an applicant.
    applicant = models.ForeignKey(Applicant, on_delete=models.deletion.CASCADE)

    # The process is a specific sequence of abstract steps that should attain the desired
    # immigration Route.
    process = models.ForeignKey(Process, on_delete=models.deletion.PROTECT)

    # Case data
    target_entry_date = models.DateField()
    target_exit_date = models.DateField()

    def can_be_offered(self):
        """
        A case can be offered iff:
        - It is not assigned to a provider
        - It is not on-offer to a provider
        """
        # TODO: This can be viewed as answering the question:
        # Given the current state of this case, does the case state machine
        # accept an 'offered-case' event which transitions to an 'on-offer' state?
        return not self.contracts.filter(rejected_at=None).exists()


class CaseStep(BaseModel):
    # Case steps are concrete steps attached to a case instance. Typically, they
    # will be in 1-1 correspondence with the abstract case.process.steps.
    # However, it may sometimes be desirable to modify a case's steps so that
    # they no longer exactly match any abstract process's steps.
    case = models.ForeignKey(
        Case, related_name="steps", on_delete=models.deletion.CASCADE
    )
    provider_contact = models.ForeignKey(
        ProviderContact, null=True, on_delete=models.deletion.SET_NULL
    )
    process_step = models.ForeignKey(ProcessStep, on_delete=models.deletion.PROTECT)
    sequence_number = models.PositiveIntegerField()
    stored_files = GenericRelation(
        StoredFile, "associated_object_id", "associated_object_content_type"
    )


class CaseContract(BaseModel):
    case = models.ForeignKey(
        Case, on_delete=models.deletion.CASCADE, related_name="contracts"
    )
    provider_contact = models.ForeignKey(
        ProviderContact, on_delete=models.deletion.CASCADE
    )
    # TODO: db-level constraint that at most one of these may be non-null
    accepted_at = models.DateTimeField(null=True)
    rejected_at = models.DateTimeField(null=True)
