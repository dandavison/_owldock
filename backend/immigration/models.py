from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, List, NewType, Optional

from django.db.models import (
    BooleanField,
    CharField,
    DecimalField,
    deletion,
    ForeignKey,
    ManyToManyField,
    PositiveIntegerField,
    TextChoices,
    UniqueConstraint,
)

from app.models import Country
from owldock.models.base import BaseModel


Activity = NewType("Activity", str)


class Location(TextChoices):
    HOME_COUNTRY = "HOME_COUNTRY", "Home Country"
    HOST_COUNTRY = "HOST_COUNTRY", "Host Country"


@dataclass
class Move:
    """
    A desired movement of an employee to a host country to perform a professional activity.
    """

    host_country: Country
    target_entry_date: Optional[datetime] = None
    target_exit_date: Optional[datetime] = None
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
        related_name="_routes_for_which_host_country",
    )

    def __str__(self):
        return f"{self.__class__.__name__}({self.host_country}: {self.name})"

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


class ProcessRuleSet(BaseModel):
    """
    A Route, and an associated collection of rules which a Move may satisfy.

    If a Move satisfies all the rules then a Process can be constructed allowing
    the Route to be used for the Move.
    """

    route = ForeignKey(Route, on_delete=deletion.CASCADE)
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
        return f"{self.__class__.__name__}({self.route}, {', '.join(data)})"

    def _satisfies_host_country(self, move: Move) -> bool:
        return move.host_country == self.route.host_country

    def _satisfies_nationalities(self, move: Move) -> bool:
        nationalities = set(self.nationalities.all())
        if not nationalities:
            return True
        return bool(set(move.nationalities) & nationalities)

    def _satisfies_contract_location(self, move: Move) -> bool:
        return self._matches(move.contract_location, self.contract_location)

    def _satisfies_duration(self, move: Move) -> bool:
        INFINITELY_LONG = timedelta(days=999999999)
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


class IssuedDocumentType(BaseModel):
    name = CharField(max_length=128, help_text="Name of this issued document type.")


class IssuedDocument(BaseModel):
    """
    A document issued on completion of a ProcessStep.
    """

    issued_document_type = ForeignKey(IssuedDocumentType, on_delete=deletion.CASCADE)
    process_step = ForeignKey("ProcessStep", on_delete=deletion.CASCADE)
    proves_right_to_enter = BooleanField(default=False)
    proves_right_to_reside = BooleanField(default=False)
    proves_right_to_work = BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.issued_document_type} ({self.process_step})"


class ProcessStep(BaseModel):
    """
    One step in a Process.
    """

    process_rule_set = ForeignKey(ProcessRuleSet, on_delete=deletion.CASCADE)
    name = CharField(max_length=128, help_text="Name of this step")
    sequence_number = PositiveIntegerField(
        help_text="Order of this step relative to other steps of this process."
    )
    issued_documents = ManyToManyField(
        IssuedDocumentType,
        through=IssuedDocument,
        help_text="Issued documents associated with this process step.",
        blank=True,
    )
    government_fee = DecimalField(
        "Government fee in host country currency",
        max_digits=9,
        decimal_places=2,
        null=True,
        blank=True,
    )
    estimated_min_duration_days = PositiveIntegerField(
        help_text="Minimum number of working days this step is expected to take"
    )
    estimated_max_duration_days = PositiveIntegerField(
        help_text="Maximum number of working days this step is expected to take"
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
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=("process_rule_set", "name"),
                name="imm__process_step__name__uniq",
            ),
        ]

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
        return (
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
