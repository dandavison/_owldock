# Regarding use of Meta.constraints rather than unique=True in the field
# declaration:
# Suppose some POST data has been received by a DRF serializer, and the plan is
# to create Service entries with get_or_create semantics. The DRF serializer
# will fail its validity check if the new Service entries look like they are
# going to try to create duplicates. But only if the unique_contraint is added
# in the Django field definition.
from django.db import models

from owldock.models.base import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=2)
    unicode_flag = models.CharField(max_length=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("name",),
                name="country__name__unique_constraint",
            ),
            models.UniqueConstraint(
                fields=("code",), name="country__code__unique_constraint"
            ),
        ]
        verbose_name_plural = "Countries"


class Activity(BaseModel):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = "Activities"


class Service(BaseModel):
    name = models.CharField(max_length=128)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("name",), name="service__name__unique_constraint"
            )
        ]


class Route(BaseModel):
    """
    E.g. 'Work Permit for France'.

    Unlike Process, this depends only on the host country
    and not on Applicant nationalities or home country.
    """

    name = models.CharField(max_length=128)
    host_country = models.ForeignKey(
        Country,
        on_delete=models.deletion.CASCADE,
        related_name="routes_for_which_host_country",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("name", "host_country"),
                name="route__host_country__name__unique_constraint",
            ),
        ]


class Process(BaseModel):
    """
    A predicted sequence of steps for a Route, given Applicant nationalities and home country.
    """

    route = models.ForeignKey(
        Route, on_delete=models.deletion.CASCADE, related_name="processes"
    )
    nationality = models.ForeignKey(
        Country,
        on_delete=models.deletion.CASCADE,
        related_name="+",
    )
    home_country = models.ForeignKey(
        Country,
        null=True,
        on_delete=models.deletion.CASCADE,
        related_name="+",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("home_country", "nationality", "route"),
                name="process__home_country__nationality__route__unique_constraint",
            ),
        ]
        verbose_name_plural = "Processes"


class ProcessStep(BaseModel):
    process = models.ForeignKey(
        Process, on_delete=models.deletion.CASCADE, related_name="steps"
    )
    service = models.ForeignKey(Service, on_delete=models.deletion.CASCADE)
    sequence_number = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("process_id", "sequence_number"),
                name="process_step__process__sequence_number__unique_constraint",
            ),
            models.UniqueConstraint(
                fields=("process_id", "service"),
                name="process_step__process__service__unique_constraint",
            ),
        ]
