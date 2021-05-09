import pytest

from app.models import Bloc
from immigration.models import Location, ProcessRuleSet, Route
from immigration.tests.factories import (
    IssuedDocumentFactory,
    IssuedDocumentTypeFactory,
    ProcessRuleSetFactory,
    ProcessRuleSetStepFactory,
    ProcessStepFactory,
    RouteFactory,
)

# TODO: substeps


@pytest.fixture()
def greece_local_hire_article_17_route(greece) -> Route:
    return RouteFactory(
        name="Local Hire Work Permit, Senior Employees (Article 17)",
        host_country=greece,
    )


@pytest.fixture()
def greece_eu_eea_swiss_national_registration_route(greece) -> Route:
    return RouteFactory(
        name="EU/EEA/Swiss National Registration",
        host_country=greece,
    )


@pytest.fixture()
def greece_technical_assignment_article_18_route(greece) -> Route:
    return RouteFactory(
        name="Technical Assignment (Article 18)",
        host_country=greece,
    )


@pytest.fixture()
def greece_local_hire_article_17_rule_set(
    greece,
    greece_local_hire_article_17_route,
) -> ProcessRuleSet:
    process_ruleset = ProcessRuleSetFactory(
        route=greece_local_hire_article_17_route,
        nationalities=Bloc.objects.get(name="non-EU").countries.all(),
        home_countries=None,
        contract_location=Location.HOST_COUNTRY,
        payroll_location=Location.HOST_COUNTRY,
        minimum_salary=None,
        duration_min_days=None,
        duration_max_days=None,
        intra_company_moves_only=False,
    )
    # Steps
    visa_step = ProcessStepFactory(
        host_country=greece,
        name="Visa Type D Application",
        estimated_min_duration_days=1,
        estimated_max_duration_days=30,
        applicant_can_enter_host_country_after=True,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=None,
        required_only_if_duration_exceeds=None,
    )
    ProcessRuleSetStepFactory(
        process_step=visa_step,
        process_ruleset=process_ruleset,
        sequence_number=1,
    )
    residence_permit_step = ProcessStepFactory(
        host_country=greece,
        name="Residence Permit for Employment",
        estimated_min_duration_days=1,
        estimated_max_duration_days=1,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=True,
        required_only_if_payroll_location=None,
        required_only_if_duration_exceeds=None,
    )
    ProcessRuleSetStepFactory(
        process_step=residence_permit_step,
        process_ruleset=process_ruleset,
        sequence_number=2,
    )
    biometrics_step = ProcessStepFactory(
        host_country=greece,
        name="Fingerprints and Biometrics Data",
        estimated_min_duration_days=90,
        estimated_max_duration_days=180,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=None,
        required_only_if_duration_exceeds=None,
    )
    ProcessRuleSetStepFactory(
        process_step=biometrics_step,
        process_ruleset=process_ruleset,
        sequence_number=3,
    )
    issuance_step = ProcessStepFactory(
        name="Issuance of Residence Card",
        estimated_min_duration_days=1,
        estimated_max_duration_days=1,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=None,
        required_only_if_duration_exceeds=None,
    )
    ProcessRuleSetStepFactory(
        process_step=issuance_step,
        process_ruleset=process_ruleset,
        sequence_number=4,
    )
    # Issued Documents
    IssuedDocumentFactory(
        issued_document_type=IssuedDocumentTypeFactory(name="D visa"),
        process_step=visa_step,
        proves_right_to_enter=True,
        proves_right_to_reside=False,
        proves_right_to_work=False,
    )
    IssuedDocumentFactory(
        issued_document_type=IssuedDocumentTypeFactory(name="Blue Receipt"),
        process_step=visa_step,
        proves_right_to_enter=False,
        proves_right_to_reside=False,
        proves_right_to_work=True,
    )
    IssuedDocumentFactory(
        issued_document_type=IssuedDocumentTypeFactory(
            name="Residence Card for Employment"
        ),
        process_step=issuance_step,
        proves_right_to_enter=False,
        proves_right_to_reside=True,
        proves_right_to_work=True,
    )
    return process_ruleset


@pytest.fixture()
def greece_eu_eea_swiss_national_registration_rule_set(
    greece,
    greece_eu_eea_swiss_national_registration_route,
) -> ProcessRuleSet:
    process_ruleset = ProcessRuleSetFactory(
        route=greece_eu_eea_swiss_national_registration_route,
        nationalities=Bloc.objects.get(name="EU").countries.all(),
        home_countries=None,
        contract_location=None,
        payroll_location=None,
        minimum_salary=None,
        duration_min_days=None,
        duration_max_days=None,
        intra_company_moves_only=False,
    )
    # Steps
    posted_worker_step = ProcessStepFactory(
        host_country=greece,
        name="Posted Worker Notification (EU/EEA)",
        estimated_min_duration_days=1,
        estimated_max_duration_days=10,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=True,
        required_only_if_payroll_location=Location.HOME_COUNTRY,
        required_only_if_duration_exceeds=None,
    )
    ProcessRuleSetStepFactory(
        process_step=posted_worker_step,
        process_ruleset=process_ruleset,
        sequence_number=1,
    )
    tax_registration_step = ProcessStepFactory(
        host_country=greece,
        name="Tax Registration",
        estimated_min_duration_days=1,
        estimated_max_duration_days=1,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=Location.HOST_COUNTRY,
        required_only_if_duration_exceeds=None,
    )
    ProcessRuleSetStepFactory(
        process_step=tax_registration_step,
        process_ruleset=process_ruleset,
        sequence_number=2,
    )
    certificate_step = ProcessStepFactory(
        host_country=greece,
        name="EU Registration Certificate",
        estimated_min_duration_days=1,
        estimated_max_duration_days=1,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=None,
        required_only_if_duration_exceeds=90,
    )
    ProcessRuleSetStepFactory(
        process_step=certificate_step,
        process_ruleset=process_ruleset,
        sequence_number=3,
    )
    # Issued Documents
    IssuedDocumentFactory(
        issued_document_type=IssuedDocumentTypeFactory(
            name="EU Registration Certificate"
        ),
        process_step=certificate_step,
        proves_right_to_enter=True,
        proves_right_to_reside=False,
        proves_right_to_work=False,
    )
    IssuedDocumentFactory(
        issued_document_type=IssuedDocumentTypeFactory(
            name="Posted Worker Notification"
        ),
        process_step=posted_worker_step,
        proves_right_to_enter=False,
        proves_right_to_reside=False,
        proves_right_to_work=False,
    )
    return process_ruleset


@pytest.fixture()
def greece_technical_assignment_article_18_route_rule_set(
    greece,
    greece_technical_assignment_article_18_route,
) -> ProcessRuleSet:
    process_ruleset = ProcessRuleSetFactory(
        route=greece_technical_assignment_article_18_route,
        nationalities=Bloc.objects.get(name="non-EU").countries.all(),
        home_countries=None,
        contract_location=Location.HOME_COUNTRY,
        payroll_location=Location.HOME_COUNTRY,
        minimum_salary=None,
        duration_min_days=None,
        duration_max_days=180,
        intra_company_moves_only=False,
    )
    # Steps
    visa_step = ProcessStepFactory(
        host_country=greece,
        name="Visa Type D Application (art. 18)",
        estimated_min_duration_days=5,
        estimated_max_duration_days=10,
        applicant_can_enter_host_country_after=True,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=None,
        required_only_if_duration_exceeds=None,
    )
    ProcessRuleSetStepFactory(
        process_step=visa_step,
        process_ruleset=process_ruleset,
        sequence_number=1,
    )
    posted_worker_step = ProcessStepFactory(
        host_country=greece,
        name="Posted Worker Notification",
        estimated_min_duration_days=1,
        estimated_max_duration_days=1,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=True,
        required_only_if_payroll_location=None,
        required_only_if_duration_exceeds=None,
    )
    ProcessRuleSetStepFactory(
        process_step=posted_worker_step,
        process_ruleset=process_ruleset,
        sequence_number=2,
    )
    # Issued Documents
    IssuedDocumentFactory(
        issued_document_type=IssuedDocumentTypeFactory(name="D visa"),
        process_step=visa_step,
        proves_right_to_enter=True,
        proves_right_to_reside=True,
        proves_right_to_work=True,
    )
    IssuedDocumentFactory(
        issued_document_type=IssuedDocumentTypeFactory(
            name="Posted Worker Notification"
        ),
        process_step=posted_worker_step,
        proves_right_to_enter=False,
        proves_right_to_reside=False,
        proves_right_to_work=False,
    )
    return process_ruleset
