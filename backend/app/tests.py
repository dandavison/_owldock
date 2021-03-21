from datetime import datetime
from datetime import timedelta

from django.core.management import call_command

import pytest

from . import api
from . import models


@pytest.mark.django_db
def test_client_contact_can_create_case():
    _setup()
    client_contact = api.ClientContact_.objects.first()
    employee = client_contact.client.employee_set.first()
    process = models.Process.objects.first()

    case = client_contact.initiate_case(
        employee_id=employee.id,
        process_id=process.id,
        host_country="Mozambique",
        target_entry_date=datetime.now() + timedelta(weeks=6),
    )
    assert case.provider_contact is None


def _setup():
    call_command("create_fake_data")