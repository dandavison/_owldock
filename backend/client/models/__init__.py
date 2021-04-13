import logging
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import deletion
from django.db.models.query import QuerySet

from app.models.process import Country, Process
from app.models.provider import Provider, ProviderContact
from owldock.models.base import BaseModel
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
    user_id = UUIDPseudoForeignKeyField(get_user_model(), to_field="uuid")
    client = models.ForeignKey(Client, on_delete=deletion.CASCADE)

    def cases(self) -> "QuerySet[Case]":
        return self.case_set.all()

    def case_steps(self) -> "QuerySet[CaseStep]":
        from client.models.case_step import CaseStep

        return CaseStep.objects.filter(case__client_contact_id=self.id)

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
            provider_id__in=[
                r.provider_id for r in self.client.provider_relationships()
            ],
            provider__routes__processes=process_id,
        ).distinct()

    def has_case_write_permission(self, case: "Case") -> bool:
        return case.client_contact == self


class Applicant(BaseModel):
    user_id = UUIDPseudoForeignKeyField(get_user_model(), to_field="uuid")
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

    @property
    def steps(self) -> "QuerySet[CaseStep]":
        return self.casestep_set.all()
