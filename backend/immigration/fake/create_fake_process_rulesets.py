# type: ignore
from app.models import Country
from immigration.tests import conftest


def create_fake_process_rulesets():
    greece = Country.objects.get(name="Greece")
    conftest.greece_local_hire_article_17_rule_set.__pytest_wrapped__.obj(
        greece,
        conftest.greece_local_hire_article_17_route.__pytest_wrapped__.obj(greece),
        conftest.greece_visa_type_D_application_step.__pytest_wrapped__.obj(greece),
        conftest.greece_residence_permit_step.__pytest_wrapped__.obj(greece),
        conftest.greece_biometrics_step.__pytest_wrapped__.obj(greece),
        conftest.greece_issuance_of_residence_card_step.__pytest_wrapped__.obj(greece),
    )
    conftest.greece_eu_eea_swiss_national_registration_rule_set.__pytest_wrapped__.obj(
        greece,
        conftest.greece_eu_eea_swiss_national_registration_route.__pytest_wrapped__.obj(
            greece
        ),
        conftest.greece_posted_worker_notification_step.__pytest_wrapped__.obj(greece),
        conftest.greece_tax_registration_step.__pytest_wrapped__.obj(greece),
        conftest.greece_eu_registration_certificate_step.__pytest_wrapped__.obj(greece),
    )
    conftest.greece_technical_assignment_article_18_route_rule_set.__pytest_wrapped__.obj(
        greece,
        conftest.greece_technical_assignment_article_18_route.__pytest_wrapped__.obj(
            greece
        ),
        conftest.greece_visa_type_D_application_step.__pytest_wrapped__.obj(greece),
        conftest.greece_posted_worker_notification_step.__pytest_wrapped__.obj(greece),
    )
