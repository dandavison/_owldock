from dataclasses import dataclass
from datetime import date, timedelta
from typing import Callable, List, NewType, Optional

from django.db.models import (
    BooleanField,
    CharField,
    DecimalField,
    deletion,
    ForeignKey,
    OneToOneField,
    ManyToManyField,
    PositiveIntegerField,
    TextChoices,
    TextField,
    UniqueConstraint,
)

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

    @property
    def duration(self) -> Optional[timedelta]:
        if self.target_entry_date and self.target_exit_date:
            return self.target_exit_date - self.target_entry_date
        else:
            return None


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

    route = ForeignKey(Route, on_delete=deletion.CASCADE)
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
    minimum_salary = DecimalField(
        "Minimum salary in host country currency",
        max_digits=9,
        decimal_places=2,
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
        data = [
            f"contract={self.contract_location}",
            f"payroll={self.payroll_location}",
        ]
        return f"{self.route}: {', '.join(data)}"

    def _satisfies_host_country(self, move: Move) -> bool:
        return move.host_country == self.route.host_country

    def _satisfies_nationalities(self, move: Move) -> bool:
        move_nationalities = set(move.nationalities or [])
        if not move_nationalities:
            return True
        nationalities = set(self.nationalities.all())
        if not nationalities:
            return True
        return bool(move_nationalities & nationalities)

    def _satisfies_contract_location(self, move: Move) -> bool:
        return self._matches(move.contract_location, self.contract_location)

    def _satisfies_duration(self, move: Move) -> bool:
        INFINITELY_LONG = timedelta(days=999999999)
        if move.target_entry_date is None:
            return True
        if move.target_exit_date is None:
            move_duration = INFINITELY_LONG
        else:
            move_duration = move.target_exit_date - move.target_entry_date

        if self.duration_min_days and move_duration.days < self.duration_min_days:
            return False
        if self.duration_max_days and move_duration.days > self.duration_max_days:
            return False
        return True

    def _satisfies_intra_company_move(self, move: Move) -> bool:
        if self.intra_company_moves_only and not move.is_intra_company:
            return False
        return True

    def _satisfies_minimum_salary(self, move: Move) -> bool:
        return self._matches(move.payroll_location, self.payroll_location)

    def _satisfies_payroll_location(self, move: Move) -> bool:
        return self._matches(move.payroll_location, self.payroll_location)

    @staticmethod
    def _matches(value_1, value_2) -> bool:
        return value_1 is None or value_2 is None or value_1 == value_2

    def get_predicates(self) -> "List[Callable[[Move], bool]]":
        """
        Return a list of predicate functions.

        A Move is defined to "satisfy" this ProcessRuleSet iff all of the
        predicate functions return True for the move.
        """
        return [
            self._satisfies_host_country,
            self._satisfies_nationalities,
            self._satisfies_contract_location,
            self._satisfies_payroll_location,
            self._satisfies_duration,
            self._satisfies_minimum_salary,
            self._satisfies_intra_company_move,
        ]

    def get_process_steps(self):
        return list(
            ProcessStep.objects.filter(processrulesetstep__process_ruleset=self)
        )


class IssuedDocument(BaseModel):
    """
    A document issued on completion of a ProcessStep.
    """

    host_country = ForeignKey(Country, on_delete=deletion.CASCADE, null=True)
    name = CharField(max_length=128, help_text="Name of this issued document.")

    proves_right_to_enter = BooleanField(default=False)
    proves_right_to_reside = BooleanField(default=False)
    proves_right_to_work = BooleanField(default=False)


class ProcessStep(BaseModel):
    """
    One step in a Process.
    """

    host_country = ForeignKey(Country, on_delete=deletion.CASCADE)
    name = CharField(max_length=128, help_text="Name of this step")
    issued_documents = ManyToManyField(
        IssuedDocument,
        help_text="Issued documents associated with this process step.",
        blank=True,
    )
    government_fee = DecimalField(
        help_text="Government fee in host country currency",
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True,
    )
    estimated_min_duration_days = PositiveIntegerField(
        help_text="Minimum number of working days this step is expected to take",
        null=True,
    )
    estimated_max_duration_days = PositiveIntegerField(
        help_text="Maximum number of working days this step is expected to take",
        null=True,
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
    required_only_if_duration_exceeds = PositiveIntegerField(
        help_text=(
            "Visit duration (days) triggering requirement for this step. "
            "Blank means no duration condition."
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

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("host_country", "name"),
                name="imm__process_step__host_country__name__uniq",
            ),
        ]

    def __str__(self) -> str:
        if self.host_country:
            return f"{self.host_country.name}: {self.name}"
        else:
            return f"<generic>: {self.name}"

    def is_required_for_move(self, move: Move) -> bool:
        """
        Should this step be included in a process for `move`?
        """
        if self._should_exclude_based_on_duration(move):
            return False
        if self._should_exclude_based_on_nationalities(move):
            return False
        return True

    def _should_exclude_based_on_duration(self, move: Move) -> bool:
        """
        Return true iff this step is triggered by duration but this move fails
        to trigger it.
        """
        return bool(
            self.required_only_if_duration_exceeds
            and move.duration
            and move.duration.days < self.required_only_if_duration_exceeds
        )

    def _should_exclude_based_on_nationalities(self, move: Move) -> bool:
        """
        Return true iff this step is triggered by nationality but this move fails
        to trigger it.
        """
        required_only_if_nationalities = set(self.required_only_if_nationalities.all())
        if required_only_if_nationalities:
            if not required_only_if_nationalities & set(move.nationalities):
                return True
        return False


class ProcessRuleSetStep(BaseModel):
    """
    A ProcessStep, in a specific ProcessRuleSet.

    In this context, the step has a sequence number that in general differs from
    the sequence number this step may have when used in a different
    ProcessRuleSet.
    """

    process_ruleset = ForeignKey(ProcessRuleSet, on_delete=deletion.CASCADE)
    process_step = ForeignKey(ProcessStep, on_delete=deletion.CASCADE)
    sequence_number = PositiveIntegerField(
        help_text="Order of this step relative to other steps of this process."
    )

    def __str__(self) -> str:
        if self.id:
            return f"{self.sequence_number}. {self.process_step.name}"
        else:
            return f"{self.sequence_number}. (New instance without process step)"


class ServiceItem(BaseModel):
    process_step = OneToOneField(ProcessStep, on_delete=deletion.CASCADE)
    description = TextField(help_text="Description of the service item")
