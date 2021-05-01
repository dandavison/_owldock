import json
from django.test import Client as DjangoTestClient

from app.models import Process, ProviderContact
from client.models import Applicant, ClientContact

# TODO: Move client tests and endpoints into the client module
from client.tests.conftest import *  # noqa
from client.tests.fake_create_case import fake_create_case_and_earmark_steps
from owldock.tests.constants import TEST_PASSWORD


def test_provider_contact_case_access(
    applicant_A: Applicant,
    client_contact_A: ClientContact,
    process_A: Process,
    provider_contact_A: ProviderContact,
    django_test_client: DjangoTestClient,
):
    # Create Case with all steps earmarked
    case = fake_create_case_and_earmark_steps(
        applicant_A, client_contact_A, process_A, provider_contact_A
    )

    # Provider contact has no access
    assert django_test_client.login(
        username=provider_contact_A.user.username,
        password=TEST_PASSWORD,
    )
    response = django_test_client.get(f"/api/provider-contact/case/{case.uuid}/")
    assert response.status_code == 403

    # Offer a step to the provider contact
    assert django_test_client.login(
        username=client_contact_A.user.username,
        password=TEST_PASSWORD,
    )
    case_step, *other_case_steps = case.steps()
    response = django_test_client.post(
        f"/api/client-contact/offer-case-step/{case_step.uuid}",
        json.dumps(
            {
                "active_contract": {
                    "provider_contact": {"uuid": str(provider_contact_A.uuid)}
                }
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert not response.json()["errors"]

    # Provider can now access the case
    assert django_test_client.login(
        username=provider_contact_A.user.username,
        password=TEST_PASSWORD,
    )
    response = django_test_client.get(f"/api/provider-contact/case/{case.uuid}/")
    assert response.status_code == 200
    assert not response.json()["errors"]

    # They can only see the step offered to them
    case_data = response.json()["data"]
    case_step_uuids = [step["uuid"] for step in case_data["steps"]]
    assert case_step_uuids == [str(case_step.uuid)]
