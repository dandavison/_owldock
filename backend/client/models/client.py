import logging
import os
import sys
from uuid import UUID
from typing import List, TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models import deletion
from django.db.models.query import QuerySet
from django_tools.middlewares.ThreadLocal import get_current_request

from app.models.process import Country, Process
from app.models.provider import Provider, ProviderContact
from owldock.models.base import BaseModel
from owldock.models.fields import UUIDPseudoForeignKeyField
from owldock.state_machine.role import Role, UserRole

if TYPE_CHECKING:
    from app.models import User
    from client.models import CaseStep

logger = logging.getLogger(__name__)


class CaseCannotBeOffered(Exception):
    pass


class Client(BaseModel):
    name = models.CharField(max_length=128)
    entity_domain_name = models.CharField(max_length=128)
    logo_url = models.URLField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("name",), name="client__name__unique_constraint"
            ),
            models.UniqueConstraint(
                fields=("entity_domain_name",),
                name="client__entity_domain_name__unique_constraint",
            ),
        ]

    def provider_relationships(self) -> "QuerySet[ClientProviderRelationship]":
        return ClientProviderRelationship.objects.filter(client=self)

    def provider_contacts(self) -> QuerySet[ProviderContact]:
        provider_uuids = [r.provider_uuid for r in self.provider_relationships()]
        return ProviderContact.objects.filter(provider__uuid__in=provider_uuids)


class ClientProviderRelationship(BaseModel):
    client = models.ForeignKey(Client, on_delete=deletion.CASCADE)
    provider_uuid = UUIDPseudoForeignKeyField(Provider)
    provider: Provider
    preferred = models.BooleanField(default=False)

    class Meta:
        unique_together = [["client", "provider_uuid"]]
        ordering = ["-preferred"]


class ClientContact(BaseModel):
    user_uuid = UUIDPseudoForeignKeyField(get_user_model())
    user: "User"

    client = models.ForeignKey(Client, on_delete=deletion.CASCADE)

    role = Role.CLIENT_CONTACT

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user_uuid",),
                name="client_contact__user_uuid__unique_constraint",
            )
        ]

    def cases(self) -> "QuerySet[Case]":
        return self.case_set.all()

    def case_steps(self) -> "QuerySet[CaseStep]":
        from client.models.case_step import CaseStep

        return CaseStep.objects.filter(case__client_contact=self)

    def case_steps_with_write_permission(self) -> "QuerySet[CaseStep]":
        return self.case_steps()

    def applicants(self) -> "QuerySet[Applicant]":
        # TODO: these are applicants for which the client contact has what permissions?
        # TODO: ClientEntity
        return Applicant.objects.filter(employer_id=self.client_id)

    def provider_relationships(self) -> QuerySet[ClientProviderRelationship]:
        return self.client.provider_relationships()

    def provider_contacts_for_process(
        self, process_uuid: UUID
    ) -> QuerySet[ProviderContact]:
        """
        Return provider contacts that can perform the process.

        These are contacts working for the client's providers.
        """
        return ProviderContact.objects.filter(
            provider__uuid__in=[
                r.provider_uuid for r in self.client.provider_relationships()
            ],
            provider__routes__processes__uuid=process_uuid,
        ).distinct()

    def provider_primary_contacts_for_process(
        self, process_uuid: UUID
    ) -> QuerySet[ProviderContact]:
        """
        Return primary provider contacts that can perform the process.

        These are the primary contacts of the subset of the client's providers
        that can perform this process.
        """
        # TODO: sort by preferred status
        provider_uuids = [r.provider_uuid for r in self.client.provider_relationships()]
        providers = Provider.objects.filter(
            uuid__in=provider_uuids, routes__processes__uuid=process_uuid
        )
        return ProviderContact.objects.filter(
            id__in=providers.values("primary_contact")
        )

    def has_case_write_permission(self, case: "Case") -> bool:
        return case.client_contact == self

    def add_uploaded_files_to_case_step(
        self,
        uploaded_files: List[UploadedFile],
        step_uuid: UUID,
    ):
        step = self.case_steps_with_write_permission().get(uuid=step_uuid)
        step.add_uploaded_files(uploaded_files, self.user, self.role)


class Applicant(BaseModel):
    user_uuid = UUIDPseudoForeignKeyField(get_user_model())
    user: "User"

    employer = models.ForeignKey(Client, on_delete=deletion.CASCADE)
    home_country_uuid = UUIDPseudoForeignKeyField(Country)
    home_country: Country

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user_uuid",), name="applicant__user_uuid__unique_constraint"
            )
        ]

    @property
    def nationalities(self) -> QuerySet[Country]:
        prefetched = getattr(self, "_prefetched_nationalities", None)
        if prefetched:
            return prefetched
        country_uuids = ApplicantNationality.objects.filter(applicant=self).values_list(
            "country_uuid", flat=True
        )
        return Country.objects.filter(uuid__in=list(country_uuids))


class ApplicantNationality(BaseModel):
    applicant = models.ForeignKey(Applicant, on_delete=deletion.CASCADE)
    country_uuid = UUIDPseudoForeignKeyField(Country)
    country: Country

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("applicant", "country_uuid"),
                name="applicant_nationality__applcant__country_uuid__unique_constraint",
            )
        ]


class Case(BaseModel):
    # TODO: created_by (ClientContact or User?)

    # A case is initiated by a client_contact. If the client contact ceases to
    # be responsible for the case, then they must be replaced with another (in a
    # single transaction, to avoid violating non-nullability of the foreign
    # key).
    client_contact = models.ForeignKey(ClientContact, on_delete=deletion.PROTECT)
    # A case is always associated with an applicant.
    applicant = models.ForeignKey(Applicant, on_delete=deletion.PROTECT)

    # The process is a specific sequence of abstract steps that should attain the desired
    # immigration Route.
    process_uuid = UUIDPseudoForeignKeyField(Process)
    process: Process

    # Case data
    target_entry_date = models.DateField()
    target_exit_date = models.DateField()

    def _all_steps(self) -> "QuerySet[CaseStep]":
        return self.casestep_set.order_by("sequence_number")

    def steps(self) -> "QuerySet[CaseStep]":
        """
        Return queryset of case steps that should be visible to the user
        responsible for the current HTTP request.
        """
        # TODO: This HTTP logic shouldn't be here; can get_queryset be used on a
        # ModelSerializer?
        request = get_current_request()
        if not request:
            assert "PYTEST_CURRENT_TEST" in os.environ
            assert "pytest" in sys.modules
            return self._all_steps()
        else:
            role = UserRole(request.user)
            assert (
                role.client_or_provider_contact
            ), "User is neither client nor provider contact"
            return role.client_or_provider_contact.case_steps().filter(case=self)
