from dataclasses import dataclass
from datetime import date, timedelta
from typing import Callable, List, NewType, Optional

import networkx as nx
from django.db.models import (
    BooleanField,
    CharField,
    deletion,
    ForeignKey,
    OneToOneField,
    Manager,
    ManyToManyField,
    PositiveIntegerField,
    Q,
    QuerySet,
    TextChoices,
    TextField,
    UniqueConstraint,
)
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from app.models import Country
from owldock.models.base import BaseModel


Activity = NewType("Activity", str)


class Location(TextChoices):
    HOME_COUNTRY = "HOME_COUNTRY", "Home Country"
    HOST_COUNTRY = "HOST_COUNTRY", "Host Country"


class RightConferredOn(TextChoices):
    APPLICATION = "Application"
    COMPLETION = "Completion"


class DataEntryStatus(TextChoices):
    NOT_STARTED = "Not started"
    DRAFT = "Draft"
    FINAL = "Final"


class ProcessStepType(TextChoices):
    PRIMARY = "Primary"
    ANCILLARY = "Ancillary"
    EVENT = "Event"
    ΤΕΛΟΣ = "ΤΕΛΟΣ"


@dataclass
class Occupation:
    name: str


# TODO: should this be a serializer?
@dataclass
class Move:
    """
    A desired movement of an employee to a host country to perform a professional activity.
    """

    host_country: Country
    target_entry_date: Optional[date] = None
    target_exit_date: Optional[date] = None
    activity: Optional[Activity] = None
    nationalities: Optional[List[Country]] = None
    contract_location: Optional[Location] = None
    payroll_location: Optional[Location] = None
    salary = Money("50000")

    def __str__(self):
        contract_location = (
            self.contract_location.name if self.contract_location else None
        )
        payroll_location = self.payroll_location.name if self.payroll_location else None
        data = [
            f"{self.nationalities} -> {self.host_country}",
            f"contract={contract_location}",
            f"payroll={payroll_location}",
        ]
        return f"{self.__class__.__name__}({', '.join(data)})"


class Route(BaseModel):
    """
    A type of immigration permission for a specific country.

    E.g. 'Work Permit for France'.
    """

    name = CharField(max_length=128)
    host_country = ForeignKey(
        Country,
        on_delete=deletion.CASCADE,
        related_name="routes_for_which_host_country",
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("name", "host_country"),
                name="immigration__route__host_country__uniq",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.host_country.name}: {self.name}"


@dataclass
class Process:
    """
    A sequence of steps that will lead to the given immigration route being attained.
    """

    route: Route
    steps: "List[ProcessStep]"

    def get_process_steps(self):
        return self.steps


class ProcessRuleSet(BaseModel):
    """
    A Route, and an associated collection of rules which a Move may satisfy.

    If a Move satisfies all the rules then a Process can be constructed allowing
    the Route to be used for the Move.
    """

    data_entry_status = CharField(
        choices=DataEntryStatus.choices,
        max_length=16,
        default=DataEntryStatus.NOT_STARTED,
    )

    route = OneToOneField(Route, on_delete=deletion.CASCADE)
    process_steps = ManyToManyField(
        "ProcessStep",
        through="ProcessRuleSetStep",
        help_text="Available steps for this process.",
    )
    nationalities = ManyToManyField(
        Country,
        help_text=(
            "Applicant nationalities for which this immigration process is available. "
            "Blank means this process is available for any applicant nationality."
        ),
        related_name="processes_for_which_nationality",
        blank=True,
    )
    home_countries = ManyToManyField(
        Country,
        help_text=(
            "Home countries for which this immigration process is available. "
            "Blank means this process is available for any home country."
        ),
        related_name="processes_for_which_home_country",
        blank=True,
    )
    contract_location = CharField(
        choices=Location.choices,
        help_text=(
            "Contract location for this process. Blank means no contract location condition."
        ),
        max_length=16,
        null=True,
        blank=True,
    )
    payroll_location = CharField(
        choices=Location.choices,
        help_text=(
            "Payroll location for this process. Blank means no payroll location condition."
        ),
        max_length=16,
        null=True,
        blank=True,
    )
    minimum_salary = MoneyField(
        help_text="Annual gross salary in host country currency",
        max_digits=14,
        decimal_places=2,
        default_currency="EUR",
        null=True,
        blank=True,
    )
    duration_min_days = PositiveIntegerField(
        help_text=(
            "Minimum visit duration (days, inclusive) required for this process to be available. "
            "Blank means no minimum duration requirement."
        ),
        null=True,
        blank=True,
    )
    duration_max_days = PositiveIntegerField(
        help_text=(
            "Maximum visit duration (days, inclusive) allowed for this process to be available. "
            "Blank means no maximum duration limit."
        ),
        null=True,
        blank=True,
    )
    intra_company_moves_only = BooleanField(
        help_text=(
            "Does this process apply only if the applicant will work in "
            "the host country for the same company as that for which "
            "they work in the home country?"
        ),
        default=False,
    )

    def __str__(self) -> str:
        return f"{self.route}"

    def get_process_steps(self):
        return list(
            ProcessStep.objects.filter(processrulesetstep__process_ruleset=self)
        )

    @property
    def step_rulesets(self) -> "List[ProcessRuleSetStep]":
        return list(self.processrulesetstep_set.all())


class IssuedDocument(BaseModel):
    """
    A document issued on completion of a ProcessStep.
    """

    host_country = ForeignKey(Country, on_delete=deletion.CASCADE, null=True)
    name = CharField(max_length=128, help_text="Name of this issued document.")

    proves_right_to_enter = BooleanField(default=False)
    proves_right_to_reside = BooleanField(default=False)
    proves_right_to_work = BooleanField(default=False)
    proves_right_to_travel_in = ManyToManyField(
        Country,
        help_text=(
            "Countries to which the holder of the document may travel. "
            "Blank means no travel rights to other countries conferred by document."
        ),
        related_name="+",
        blank=True,
    )


class ProcessStepManager(Manager):
    def get_for_host_country_codes(
        self, country_codes: List[str]
    ) -> "QuerySet[ProcessStep]":
        return self.filter(
            Q(host_country__code__in=country_codes) | Q(host_country__isnull=True)
        )

    def dependency_cycles(self):
        graph = nx.DiGraph()
        for dependency in ProcessStep.depends_on.through.objects.select_related(
            "from_processstep", "to_processstep"
        ).all():
            graph.add_edge(dependency.from_processstep, dependency.to_processstep)
        return list(nx.simple_cycles(graph))


class ProcessStep(BaseModel):
    """
    One step in a Process.
    """

    host_country = ForeignKey(
        Country, null=True, blank=True, on_delete=deletion.CASCADE
    )
    name = CharField(max_length=128, help_text="Name of this step")
    type = CharField(
        choices=ProcessStepType.choices,
        max_length=16,
    )
    depends_on = ManyToManyField(
        "ProcessStep",
        help_text="Steps on which this step depends directly.",
        blank=True,
    )
    issued_documents = ManyToManyField(
        IssuedDocument,
        help_text="Issued documents associated with this process step.",
        blank=True,
    )
    government_fee = MoneyField(
        help_text="Government fee in host country currency",
        max_digits=14,
        decimal_places=2,
        default_currency="EUR",
        null=True,
        blank=True,
    )
    estimated_min_duration_days = PositiveIntegerField(
        help_text="Minimum number of working days this step is expected to take",
        null=True,
        blank=True,
    )
    estimated_max_duration_days = PositiveIntegerField(
        help_text="Maximum number of working days this step is expected to take",
        null=True,
        blank=True,
    )
    applicant_can_enter_host_country_on = CharField(
        choices=RightConferredOn.choices,
        max_length=16,
        null=True,
        blank=True,
    )
    applicant_can_work_in_host_country_on = CharField(
        choices=RightConferredOn.choices,
        max_length=16,
        null=True,
        blank=True,
    )
    applicant_can_enter_host_country_after = BooleanField(
        help_text="Can the applicant enter the host country on completion of this step?",
        default=False,
    )
    applicant_can_work_in_host_country_after = BooleanField(
        help_text="Can the applicant work in the host country on completion of this step?",
        default=False,
    )
    required_only_if_contract_location = CharField(
        choices=Location.choices,
        help_text=(
            "Contract location triggering requirement for this step. "
            "Blank means no contract location condition."
        ),
        max_length=16,
        null=True,
        blank=True,
    )
    required_only_if_payroll_location = CharField(
        choices=Location.choices,
        help_text=(
            "Payroll location triggering requirement for this step. "
            "Blank means no payroll location condition."
        ),
        max_length=16,
        null=True,
        blank=True,
    )
    required_only_if_duration_less_than = PositiveIntegerField(
        help_text=(
            "Maximum visit duration (days) triggering requirement for this step. "
            "Blank means no maximum duration condition."
        ),
        null=True,
        blank=True,
    )
    required_only_if_duration_greater_than = PositiveIntegerField(
        help_text=(
            "Minimum visit duration (days) triggering requirement for this step. "
            "Blank means no minimum duration condition."
        ),
        null=True,
        blank=True,
    )
    required_only_if_nationalities = ManyToManyField(
        Country,
        help_text=(
            "Applicant nationalities triggering requirement for this step. "
            "Blank means no nationality condition."
        ),
        blank=True,
        related_name="+",
    )
    required_only_if_home_country = ManyToManyField(
        Country,
        help_text=(
            "Applicant home countries triggering requirement for this step. "
            "Blank means no home country condition."
        ),
        blank=True,
        related_name="+",
    )

    _prefetched_depends_on: "List[ProcessStep]"

    objects = ProcessStepManager()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("host_country", "name"),
                name="imm__process_step__host_country__name__uniq",
            ),
        ]

    def __str__(self) -> str:
        if self.type == ProcessStepType.EVENT:
            return f"{self.type}: {self.name}"
        else:
            host_country = (
                self.host_country.name if self.host_country else "(No host country)"
            )
            return f"{host_country} {self.type}: {self.name}"

    @property
    def step_duration_range(self) -> List[Optional[int]]:
        return [self.estimated_min_duration_days, self.estimated_max_duration_days]

    @property
    def step_government_fee(self) -> List[Optional[int]]:
        return self.government_fee

    @property
    def depends_on_ids(self) -> List[int]:
        try:
            prefetched = self._prefetched_depends_on
        except AttributeError:
            prefetched = list(self.depends_on.all())
        return [obj.id for obj in prefetched]


class ProcessRuleSetStep(BaseModel):
    """
    A ProcessStep, in a specific ProcessRuleSet.

    In this context, the step has a sequence number that in general differs from
    the sequence number this step may have when used in a different
    ProcessRuleSet.
    """

    process_ruleset = ForeignKey(ProcessRuleSet, on_delete=deletion.CASCADE)
    process_step = ForeignKey(ProcessStep, on_delete=deletion.CASCADE)

    def __str__(self) -> str:
        if self.id:
            return self.process_step.name
        else:
            return "(New instance without process step)"


class ServiceItem(BaseModel):
    process_step = OneToOneField(ProcessStep, on_delete=deletion.CASCADE)
    description = TextField(help_text="Description of the service item")
