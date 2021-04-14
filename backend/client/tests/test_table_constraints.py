import pytest

from django.db import IntegrityError


def test_applicant_table_constraints(applicant_A, applicant_B):
    applicant_A.user_uuid = applicant_B.user_uuid
    with pytest.raises(IntegrityError):
        applicant_A.save()


def test_client_table_constraints(client_A, client_B):
    client_A.name = client_B.name
    with pytest.raises(IntegrityError):
        client_A.save()


def test_client_contact_table_constraints(client_contact_A, client_contact_B):
    client_contact_A.user_uuid = client_contact_B.user_uuid
    with pytest.raises(IntegrityError):
        client_contact_A.save()
