# type: ignore
from app.models import Country
from immigration.tests import conftest


def create_fake_process_rulesets():
    greece = Country.objects.get(name="Greece")
    conftest.greece_local_hire_article_17_rule_set.__pytest_wrapped__.obj(
        conftest.greece_local_hire_article_17_route.__pytest_wrapped__.obj(greece)
    )
    conftest.greece_eu_eea_swiss_national_registration_rule_set.__pytest_wrapped__.obj(
        conftest.greece_eu_eea_swiss_national_registration_route.__pytest_wrapped__.obj(
            greece
        )
    )
    conftest.greece_technical_assignment_article_18_route_rule_set.__pytest_wrapped__.obj(
        conftest.greece_technical_assignment_article_18_route.__pytest_wrapped__.obj(
            greece
        )
    )
