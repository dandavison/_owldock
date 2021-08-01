# type: ignore
from app.models import Country
from immigration.tests import conftest
from conftest import brazil as brazil_fixture
from conftest import brazil_bloc as brazil_bloc_fixture
from conftest import france as france_fixture
from conftest import france_bloc as france_bloc_fixture


def create_fake_process_rulesets():
    greece = Country.objects.get(name="Greece")
    greece_visa_type_d = conftest.greece_visa_type_D.__pytest_wrapped__.obj(greece)
    greece_blue_receipt = conftest.greece_blue_receipt.__pytest_wrapped__.obj(greece)
    greece_visa_type_D_application_step = (
        conftest.greece_visa_type_D_application_step.__pytest_wrapped__.obj(
            greece,
            greece_visa_type_d,
            greece_blue_receipt,
        )
    )

    greece_residence_card = conftest.greece_residence_card.__pytest_wrapped__.obj(
        greece
    )
    greece_issuance_of_residence_card_step = (
        conftest.greece_issuance_of_residence_card_step.__pytest_wrapped__.obj(
            greece, greece_residence_card
        )
    )
    greece_posted_worker_notification = (
        conftest.greece_posted_worker_notification.__pytest_wrapped__.obj(greece)
    )
    greece_posted_worker_notification_step = (
        conftest.greece_posted_worker_notification_step.__pytest_wrapped__.obj(
            greece, greece_posted_worker_notification
        )
    )
    greece_eu_registration_certificate = (
        conftest.greece_eu_registration_certificate.__pytest_wrapped__.obj(greece)
    )

    brazil = brazil_fixture.__pytest_wrapped__.obj()
    brazil_bloc = brazil_bloc_fixture.__pytest_wrapped__.obj(brazil)
    france = france_fixture.__pytest_wrapped__.obj()
    france_bloc = france_bloc_fixture.__pytest_wrapped__.obj(france)
    conftest.greece_local_hire_article_17_rule_set.__pytest_wrapped__.obj(
        greece,
        brazil_bloc,
        conftest.greece_local_hire_article_17_route.__pytest_wrapped__.obj(greece),
        greece_visa_type_D_application_step,
        conftest.greece_residence_permit_step.__pytest_wrapped__.obj(greece),
        conftest.greece_biometrics_step.__pytest_wrapped__.obj(greece),
        greece_issuance_of_residence_card_step,
    )
    conftest.greece_eu_eea_swiss_national_registration_rule_set.__pytest_wrapped__.obj(
        greece,
        france_bloc,
        conftest.greece_eu_eea_swiss_national_registration_route.__pytest_wrapped__.obj(
            greece
        ),
        greece_posted_worker_notification_step,
        conftest.greece_tax_registration_step.__pytest_wrapped__.obj(greece),
        conftest.greece_eu_registration_certificate_step.__pytest_wrapped__.obj(
            greece, greece_eu_registration_certificate
        ),
    )
    conftest.greece_technical_assignment_article_18_route_rule_set.__pytest_wrapped__.obj(
        greece,
        brazil_bloc,
        conftest.greece_technical_assignment_article_18_route.__pytest_wrapped__.obj(
            greece
        ),
        greece_visa_type_D_application_step,
        greece_posted_worker_notification_step,
    )
