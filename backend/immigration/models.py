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


class Location(TextChoices):
    HOME_COUNTRY = "HOME_COUNTRY", "Home Country"
    HOST_COUNTRY = "HOST_COUNTRY", "Host Country"


class IssuedDocumentType(BaseModel):
    name = CharField(max_length=128, help_text="Name of this issued document type.")


class IssuedDocument(BaseModel):
    issued_document_type = ForeignKey(IssuedDocumentType, on_delete=deletion.CASCADE)
    process = ForeignKey("Process", on_delete=deletion.CASCADE)
    proves_right_to_enter = BooleanField(default=False)
    proves_right_to_reside = BooleanField(default=False)
    proves_right_to_work = BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.issued_document_type} ({self.process})"


# Note: this corresponds to app.models.Route, not to app.models.Process
class Process(BaseModel):
    """
    E.g. 'Work Permit for France'.
    """

    name = CharField(help_text="Name of this immigration process", max_length=128)
    host_country = ForeignKey(
        Country,
        help_text="Host country for this immigration process",
        on_delete=deletion.CASCADE,
        related_name="processes_for_which_host_country",
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
    issued_documents = ManyToManyField(
        IssuedDocumentType,
        through=IssuedDocument,
        help_text="Issued documents associated with this process.",
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
            "Minimum visit duration (days) required for this process to be available. "
            "Blank means no minimum duration requirement."
        ),
        null=True,
        blank=True,
    )
    duration_max_days = PositiveIntegerField(
        help_text=(
            "Maximum visit duration (days) allowed for this process to be available. "
            "Blank means no maximum duration limit."
        ),
        null=True,
        blank=True,
    )
    intra_company_relationship_required = BooleanField(
        help_text=(
            "Does this process apply only if the applicant will work in "
            "the host country for the same company as that for which "
            "they work in the    home country?"
        ),
        default=False,
    )

    class Meta:
        verbose_name_plural = "Processes"
        constraints = [
            UniqueConstraint(
                fields=("name", "host_country"),
                name="imm__process__host_country_name__uniq",
            ),
        ]


class ProcessStep(BaseModel):
    process = ForeignKey(Process, on_delete=deletion.CASCADE)
    name = CharField(max_length=128, help_text="Name of this step")
    sequence_number = PositiveIntegerField(
        help_text="Order of this step relative to other steps of this process."
    )
    estimated_min_duration_days = PositiveIntegerField(
        help_text="Minimum number of days this step is expected to take"
    )
    estimated_max_duration_days = PositiveIntegerField(
        help_text="Maximum number of days this step is expected to take"
    )
    applicant_can_enter_host_country_after = BooleanField(
        help_text="Can the applicant enter the host country on completion of this step?",
        default=False,
    )
    applicant_can_work_after = BooleanField(
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
                fields=("process", "name"),
                name="imm__process_step__name__uniq",
            ),
            UniqueConstraint(
                fields=("process", "sequence_number"),
                name="imm__process_step__sequence_number__uniq",
            ),
        ]
