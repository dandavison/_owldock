import pytest

from immigration.models import (
    IssuedDocument,
    Location,
    ProcessRuleSet,
    ProcessStep,
    Route,
)
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
def greece_visa_type_D(greece) -> IssuedDocument:
    return IssuedDocumentFactory(
        name="Visa Type D",
        proves_right_to_enter=True,
        proves_right_to_reside=False,
        proves_right_to_work=False,
    )


@pytest.fixture()
def greece_blue_receipt(greece) -> IssuedDocument:
    return IssuedDocumentFactory(
        name="Blue Receipt",
        proves_right_to_enter=False,
        proves_right_to_reside=False,
        proves_right_to_work=True,
    )


@pytest.fixture()
def greece_residence_card(greece) -> IssuedDocument:
    return IssuedDocumentFactory(
        name="Residence Card for Employment",
        proves_right_to_enter=False,
        proves_right_to_reside=True,
        proves_right_to_work=True,
    )


@pytest.fixture()
def greece_eu_registration_certificate(greece) -> IssuedDocument:
    return IssuedDocumentFactory(
        name="EU Registration Certificate",
        proves_right_to_enter=True,
        proves_right_to_reside=False,
        proves_right_to_work=False,
    )


@pytest.fixture()
def greece_posted_worker_notification(greece) -> IssuedDocument:
    return IssuedDocumentFactory(
        name="Posted Worker Notification",
        proves_right_to_enter=False,
        proves_right_to_reside=False,
        proves_right_to_work=False,
    )


@pytest.fixture()
def greece_visa_type_D_application_step(
    greece, greece_visa_type_D, greece_blue_receipt
) -> ProcessStep:
    step = ProcessStepFactory(
        host_country=greece,
        name="Visa Type D Application",
        estimated_min_duration_days=1,
        estimated_max_duration_days=30,
        applicant_can_enter_host_country_after=True,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=None,
        required_only_if_duration_less_than=None,
        required_only_if_duration_greater_than=None,
    )
    step.issued_documents.add(greece_visa_type_D)
    step.issued_documents.add(greece_blue_receipt)
    return step


@pytest.fixture()
def greece_posted_worker_notification_step(
    greece, greece_posted_worker_notification
) -> ProcessStep:
    step = ProcessStepFactory(
        host_country=greece,
        name="Posted Worker Notification (EU/EEA)",
        estimated_min_duration_days=1,
        estimated_max_duration_days=10,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=True,
        required_only_if_payroll_location=Location.HOME_COUNTRY,
        required_only_if_duration_less_than=None,
        required_only_if_duration_greater_than=None,
    )
    step.issued_documents.add(greece_posted_worker_notification)
    return step


@pytest.fixture()
def brazil_step(brazil) -> ProcessStep:
    return ProcessStepFactory(host_country=brazil, name="Entry")


@pytest.fixture()
def france_step(france) -> ProcessStep:
    return ProcessStepFactory(host_country=france, name="Entry")


@pytest.fixture()
def entry_step(brazil_step, france_step) -> ProcessStep:
    entry_step = ProcessStepFactory(host_country=None, name="Entry")
    entry_step.depends_on.set([brazil_step, france_step])
    return entry_step


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
        required_only_if_duration_less_than=None,
        required_only_if_duration_greater_than=None,
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
        required_only_if_duration_less_than=None,
        required_only_if_duration_greater_than=None,
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
        required_only_if_duration_less_than=None,
        required_only_if_duration_greater_than=None,
    )


@pytest.fixture()
def greece_issuance_of_residence_card_step(
    greece, greece_residence_card
) -> ProcessStep:
    step = ProcessStepFactory(
        host_country=greece,
        name="Issuance of Residence Card",
        estimated_min_duration_days=1,
        estimated_max_duration_days=1,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=None,
        required_only_if_duration_less_than=None,
        required_only_if_duration_greater_than=None,
    )
    step.issued_documents.add(greece_residence_card)
    return step


@pytest.fixture()
def greece_eu_registration_certificate_step(
    greece, greece_eu_registration_certificate
) -> ProcessStep:
    step = ProcessStepFactory(
        host_country=greece,
        name="EU Registration Certificate",
        estimated_min_duration_days=1,
        estimated_max_duration_days=1,
        applicant_can_enter_host_country_after=False,
        applicant_can_work_in_host_country_after=False,
        required_only_if_payroll_location=None,
        required_only_if_duration_less_than=None,
        required_only_if_duration_greater_than=90,
    )
    step.issued_documents.add(greece_eu_registration_certificate)
    return step


@pytest.fixture()
def greece_local_hire_article_17_rule_set(
    greece,
    brazil_bloc,
    greece_local_hire_article_17_route,
    greece_visa_type_D_application_step,
    greece_residence_permit_step,
    greece_biometrics_step,
    greece_issuance_of_residence_card_step,
) -> ProcessRuleSet:
    process_ruleset = ProcessRuleSetFactory(
        route=greece_local_hire_article_17_route,
        nationalities=brazil_bloc.countries.all(),  # In reality this is non-EU
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
    )
    ProcessRuleSetStepFactory(
        process_step=greece_residence_permit_step,
        process_ruleset=process_ruleset,
    )
    ProcessRuleSetStepFactory(
        process_step=greece_biometrics_step,
        process_ruleset=process_ruleset,
    )
    ProcessRuleSetStepFactory(
        process_step=greece_issuance_of_residence_card_step,
        process_ruleset=process_ruleset,
    )
    return process_ruleset


@pytest.fixture()
def greece_eu_eea_swiss_national_registration_rule_set(
    greece,
    france_bloc,
    greece_eu_eea_swiss_national_registration_route,
    greece_posted_worker_notification_step,
    greece_tax_registration_step,
    greece_eu_registration_certificate_step,
) -> ProcessRuleSet:
    process_ruleset = ProcessRuleSetFactory(
        route=greece_eu_eea_swiss_national_registration_route,
        nationalities=france_bloc.countries.all(),  # In reality this is EU
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
    )
    ProcessRuleSetStepFactory(
        process_step=greece_tax_registration_step,
        process_ruleset=process_ruleset,
    )
    ProcessRuleSetStepFactory(
        process_step=greece_eu_registration_certificate_step,
        process_ruleset=process_ruleset,
    )
    return process_ruleset


@pytest.fixture()
def greece_technical_assignment_article_18_route_rule_set(
    greece,
    brazil_bloc,
    greece_technical_assignment_article_18_route,
    greece_visa_type_D_application_step,
    greece_posted_worker_notification_step,
) -> ProcessRuleSet:
    process_ruleset = ProcessRuleSetFactory(
        route=greece_technical_assignment_article_18_route,
        nationalities=brazil_bloc.countries.all(),  # In reality this is non-EU
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
    )
    ProcessRuleSetStepFactory(
        process_step=greece_posted_worker_notification_step,
        process_ruleset=process_ruleset,
    )
    return process_ruleset
