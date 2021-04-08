from django.db import models

from owldock.models import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=2)
    unicode_flag = models.CharField(max_length=2)


class Activity(BaseModel):
    name = models.CharField(max_length=128)


class Service(BaseModel):
    name = models.CharField(max_length=128)


class Route(BaseModel):
    """
    E.g. 'Work Permit for France'.

    Unlike Process, this depends only on the host country
    and not on Applicant nationalities or home country.
    """

    name = models.CharField(max_length=128)
    host_country = models.ForeignKey(
        Country,
        on_delete=models.deletion.PROTECT,
        related_name="routes_for_which_host_country",
    )


class Process(BaseModel):
    """
    A predicted sequence of steps for a Route, given Applicant nationalities and home country.
    """

    route = models.ForeignKey(
        Route, on_delete=models.deletion.PROTECT, related_name="processes"
    )
    nationality = models.ForeignKey(
        Country,
        on_delete=models.deletion.PROTECT,
        related_name="processes_for_which_nationality",
    )
    home_country = models.ForeignKey(
        Country,
        null=True,
        on_delete=models.deletion.PROTECT,
        related_name="processes_for_which_home_country",
    )


class ProcessStep(BaseModel):
    process = models.ForeignKey(
        Process, on_delete=models.deletion.PROTECT, related_name="steps"
    )
    service = models.ForeignKey(Service, on_delete=models.deletion.CASCADE)
    sequence_number = models.PositiveIntegerField()
