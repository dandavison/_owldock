import pytest

from app.models import Bloc
from immigration.models import Location, ProcessRuleSet, ProcessStep, Route
from immigration.tests.factories import (
    IssuedDocumentFactory,
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
def greece_visa_type_D_application_step(greece) -> ProcessStep:
    return ProcessStepFactory(
        host_country=greece,
        name="Visa Type D Application",
        estimated_min_duration_days=1,
        estimated_max_duration_days=30,
        applicant_can_enter_host_country_after=True,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=None,
        required_only_if_duration_exceeds=None,
    )


@pytest.fixture()
def greece_posted_worker_notification_step(greece) -> ProcessStep:
    return ProcessStepFactory(
        host_country=greece,
        name="Posted Worker Notification (EU/EEA)",
        estimated_min_duration_days=1,
        estimated_max_duration_days=10,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=True,
        required_only_if_payroll_location=Location.HOME_COUNTRY,
        required_only_if_duration_exceeds=None,
    )


@pytest.fixture()
def greece_residence_permit_step(greece) -> ProcessStep:
    return ProcessStepFactory(
        host_country=greece,
        name="Residence Permit for Employment",
        estimated_min_duration_days=1,
        estimated_max_duration_days=1,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=True,
        required_only_if_payroll_location=None,
        required_only_if_duration_exceeds=None,
    )


@pytest.fixture()
def greece_tax_registration_step(greece) -> ProcessStep:
    return ProcessStepFactory(
        host_country=greece,
        name="Tax Registration",
        estimated_min_duration_days=1,
        estimated_max_duration_days=1,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=Location.HOST_COUNTRY,
        required_only_if_duration_exceeds=None,
    )


@pytest.fixture()
def greece_biometrics_step(greece) -> ProcessStep:
    return ProcessStepFactory(
        host_country=greece,
        name="Fingerprints and Biometrics Data",
        estimated_min_duration_days=90,
        estimated_max_duration_days=180,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=None,
        required_only_if_duration_exceeds=None,
    )


@pytest.fixture()
def greece_issuance_of_residence_card_step(greece) -> ProcessStep:
    return ProcessStepFactory(
        name="Issuance of Residence Card",
        estimated_min_duration_days=1,
        estimated_max_duration_days=1,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=None,
        required_only_if_duration_exceeds=None,
    )


@pytest.fixture()
def greece_eu_registration_certificate_step(greece) -> ProcessStep:
    return ProcessStepFactory(
        host_country=greece,
        name="EU Registration Certificate",
        estimated_min_duration_days=1,
        estimated_max_duration_days=1,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=None,
        required_only_if_duration_exceeds=90,
    )


@pytest.fixture()
def greece_local_hire_article_17_rule_set(
    greece,
    greece_local_hire_article_17_route,
    greece_visa_type_D_application_step,
    greece_residence_permit_step,
    greece_biometrics_step,
    greece_issuance_of_residence_card_step,
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
    ProcessRuleSetStepFactory(
        process_step=greece_visa_type_D_application_step,
        process_ruleset=process_ruleset,
        sequence_number=1,
    )
    ProcessRuleSetStepFactory(
        process_step=greece_residence_permit_step,
        process_ruleset=process_ruleset,
        sequence_number=2,
    )
    ProcessRuleSetStepFactory(
        process_step=greece_biometrics_step,
        process_ruleset=process_ruleset,
        sequence_number=3,
    )
    ProcessRuleSetStepFactory(
        process_step=greece_issuance_of_residence_card_step,
        process_ruleset=process_ruleset,
        sequence_number=4,
    )
    # Issued Documents
    IssuedDocumentFactory(
        name="D visa",
        process_step=greece_visa_type_D_application_step,
        proves_right_to_enter=True,
        proves_right_to_reside=False,
        proves_right_to_work=False,
    )
    IssuedDocumentFactory(
        name="Blue Receipt",
        process_step=greece_visa_type_D_application_step,
        proves_right_to_enter=False,
        proves_right_to_reside=False,
        proves_right_to_work=True,
    )
    IssuedDocumentFactory(
        name="Residence Card for Employment",
        process_step=greece_issuance_of_residence_card_step,
        proves_right_to_enter=False,
        proves_right_to_reside=True,
        proves_right_to_work=True,
    )
    return process_ruleset


@pytest.fixture()
def greece_eu_eea_swiss_national_registration_rule_set(
    greece,
    greece_eu_eea_swiss_national_registration_route,
    greece_posted_worker_notification_step,
    greece_tax_registration_step,
    greece_eu_registration_certificate_step,
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
    ProcessRuleSetStepFactory(
        process_step=greece_posted_worker_notification_step,
        process_ruleset=process_ruleset,
        sequence_number=1,
    )
    ProcessRuleSetStepFactory(
        process_step=greece_tax_registration_step,
        process_ruleset=process_ruleset,
        sequence_number=2,
    )
    ProcessRuleSetStepFactory(
        process_step=greece_eu_registration_certificate_step,
        process_ruleset=process_ruleset,
        sequence_number=3,
    )
    # Issued Documents
    IssuedDocumentFactory(
        name="EU Registration Certificate",
        process_step=greece_eu_registration_certificate_step,
        proves_right_to_enter=True,
        proves_right_to_reside=False,
        proves_right_to_work=False,
    )
    IssuedDocumentFactory(
        name="Posted Worker Notification",
        process_step=greece_posted_worker_notification_step,
        proves_right_to_enter=False,
        proves_right_to_reside=False,
        proves_right_to_work=False,
    )
    return process_ruleset


@pytest.fixture()
def greece_technical_assignment_article_18_route_rule_set(
    greece,
    greece_technical_assignment_article_18_route,
    greece_visa_type_D_application_step,
    greece_posted_worker_notification_step,
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
    ProcessRuleSetStepFactory(
        process_step=greece_visa_type_D_application_step,
        process_ruleset=process_ruleset,
        sequence_number=1,
    )
    ProcessRuleSetStepFactory(
        process_step=greece_posted_worker_notification_step,
        process_ruleset=process_ruleset,
        sequence_number=2,
    )
    # Issued Documents
    IssuedDocumentFactory(
        name="D visa",
        process_step=greece_visa_type_D_application_step,
        proves_right_to_enter=True,
        proves_right_to_reside=True,
        proves_right_to_work=True,
    )
    IssuedDocumentFactory(
        name="Posted Worker Notification",
        process_step=greece_posted_worker_notification_step,
        proves_right_to_enter=False,
        proves_right_to_reside=False,
        proves_right_to_work=False,
    )
    return process_ruleset
