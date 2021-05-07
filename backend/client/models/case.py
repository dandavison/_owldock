from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import deletion
from django.db.models.query import QuerySet
from typing import TYPE_CHECKING

from app.models import Country
from immigration.models import Move, ProcessRuleSet
from owldock.models.base import BaseModel
from owldock.models.fields import UUIDPseudoForeignKeyField

if TYPE_CHECKING:
    from app.models import User


class Applicant(BaseModel):
    user_uuid = UUIDPseudoForeignKeyField(get_user_model())
    user: "User"

    employer = models.ForeignKey("Client", on_delete=deletion.CASCADE)
    home_country_uuid = UUIDPseudoForeignKeyField(Country)
    home_country: Country

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user_uuid",), name="applicant__user_uuid__unique_constraint"
            )
        ]

    def validate(self):
        # TODO: Should UUIDPseudoForeignKeyField cause this to happen
        # automatically?
        assert (
            self.user_uuid
            and get_user_model().objects.filter(uuid=self.user_uuid).exists()
        )
        assert (
            self.home_country_uuid
            and Country.objects.filter(uuid=self.home_country_uuid).exists()
        )

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
        verbose_name_plural = "ApplicantNationalities"

    def validate(self):
        assert (
            self.country_uuid
            and Country.objects.filter(uuid=self.country_uuid).exists()
        )


class Case(BaseModel):
    # TODO: created_by (ClientContact or User?)

    # A case is initiated by a client_contact. If the client contact ceases to
    # be responsible for the case, then they must be replaced with another (in a
    # single transaction, to avoid violating non-nullability of the foreign
    # key).
    client_contact = models.ForeignKey("ClientContact", on_delete=deletion.CASCADE)
    # A case is always associated with an applicant.
    applicant = models.ForeignKey(Applicant, on_delete=deletion.CASCADE)

    # The process is a specific sequence of abstract steps that should attain the desired
    # immigration Route.
    process_uuid = UUIDPseudoForeignKeyField(ProcessRuleSet)
    process: ProcessRuleSet

    # Case data
    target_entry_date = models.DateField()
    target_exit_date = models.DateField()

    @property
    def move(self) -> Move:
        return Move(
            host_country=self.process.route.host_country,
            target_entry_date=self.target_entry_date,
            target_exit_date=self.target_exit_date,
            nationalities=list(self.applicant.nationalities.all()),
            activity=None,
            contract_location=None,
            payroll_location=None,
        )

    def validate(self):
        # TODO: Should UUIDPseudoForeignKeyField cause this to happen
        # automatically?
        assert (
            self.process_uuid
            and ProcessRuleSet.objects.filter(uuid=self.process_uuid).exists()
        )
