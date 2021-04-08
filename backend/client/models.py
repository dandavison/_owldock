import logging
from typing import List
from uuid import UUID

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import deletion
from django.db.models.query import QuerySet
from django.db.transaction import atomic

from app.models.process import Country, Process, ProcessStep, Route
from app.models.provider import Provider, ProviderContact
from app.models.file import StoredFile
from owldock.models import BaseModel
from owldock.models.fields import UUIDPseudoForeignKeyField


logger = logging.getLogger(__name__)


class CaseCannotBeOffered(Exception):
    pass


class Client(BaseModel):
    name = models.CharField(max_length=128)
    entity_domain_name = models.CharField(max_length=128)
    logo_url = models.URLField()

    def provider_relationships(self) -> "QuerySet[ClientProviderRelationship]":
        return ClientProviderRelationship.objects.filter(client_id=self.id)

    def provider_contacts(self) -> QuerySet[ProviderContact]:
        provider_ids = [r.id for r in self.provider_relationships()]
        return ProviderContact.objects.filter(provider_id__in=provider_ids)


class ClientProviderRelationship(BaseModel):
    client = models.ForeignKey(Client, on_delete=deletion.CASCADE)
    provider_id = UUIDPseudoForeignKeyField(Provider)
    preferred = models.BooleanField(default=False)

    class Meta:
        unique_together = [["client", "provider_id"]]
        ordering = ["-preferred"]


class ClientContact(BaseModel):
    user_id = UUIDPseudoForeignKeyField(get_user_model())
    client = models.ForeignKey(Client, on_delete=deletion.CASCADE)

    def applicants(self) -> "QuerySet[Applicant]":
        # TODO: these are applicants for which the client contact has what permissions?
        # TODO: ClientEntity
        return Applicant.objects.filter(employer_id=self.client_id)

    def provider_relationships(self) -> QuerySet[ClientProviderRelationship]:
        return self.client.provider_relationships()

    # TODO: provider contacts perform steps, not necessarily entire processes.
    def provider_contacts_for_process(
        self, process_id: UUID
    ) -> QuerySet[ProviderContact]:
        """
        Return suggested provider contacts that can perform the process.

        These are contacts working for the client's providers. They are sorted
        by preferred status with ties broken alphabetically.
        """
        return ProviderContact.objects.filter(
            provider_id__in=self.client.provider_relationships().values("provider_id"),
            provider__routes__processes=process_id,
        ).distinct()

    @property
    def cases_with_read_permission(self) -> "QuerySet[Case]":
        return self.case_set.all()

    # TODO: move to serializer?
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
        CaseContract.objects.create(case=case, provider_contact_id=provider_contact.id)

    def has_case_write_permission(self, case: "Case") -> bool:
        return case.client_contact == self


class Applicant(BaseModel):
    user_id = UUIDPseudoForeignKeyField(get_user_model())
    employer = models.ForeignKey(Client, on_delete=deletion.CASCADE)
    home_country_id = UUIDPseudoForeignKeyField(Country)

    @property
    def nationalities(self) -> QuerySet[Country]:
        country_ids = ApplicantNationality.objects.filter(applicant=self).values_list(
            "country_id", flat=True
        )
        return Country.objects.filter(id__in=list(country_ids))


class ApplicantNationality(BaseModel):
    applicant = models.ForeignKey(Applicant, on_delete=deletion.CASCADE)
    country_id = UUIDPseudoForeignKeyField(Country)


class Case(BaseModel):
    # TODO: created_by (ClientContact or User?)

    # A case is initiated by a client_contact and it will usually stay non-null.
    # It may become null if a ClientContact ceases to be employed by a Client.
    client_contact = models.ForeignKey(
        ClientContact, null=True, on_delete=deletion.SET_NULL
    )
    # A case is always associated with an applicant.
    applicant = models.ForeignKey(Applicant, on_delete=deletion.CASCADE)

    # The process is a specific sequence of abstract steps that should attain the desired
    # immigration Route.
    process_id = UUIDPseudoForeignKeyField(Process)

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
    case = models.ForeignKey(Case, related_name="steps", on_delete=deletion.CASCADE)
    provider_contact_id = UUIDPseudoForeignKeyField(ProviderContact, null=True)
    process_step_id = UUIDPseudoForeignKeyField(ProcessStep)
    sequence_number = models.PositiveIntegerField()

    @property
    def stored_files(self) -> QuerySet[StoredFile]:
        # GenericRelation is not working with our multiple database setup
        return StoredFile.objects.filter(
            associated_object_id=self.id,
            associated_object_content_type=ContentType.objects.get_for_model(CaseStep),
        )


class CaseContract(BaseModel):
    case = models.ForeignKey(Case, on_delete=deletion.CASCADE, related_name="contracts")
    provider_contact_id = UUIDPseudoForeignKeyField(ProviderContact)
    # TODO: db-level constraint that at most one of these may be non-null
    accepted_at = models.DateTimeField(null=True)
    rejected_at = models.DateTimeField(null=True)
