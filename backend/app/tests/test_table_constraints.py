import pytest

from django.db import IntegrityError


def test_country_table_name_constraint(country_A, country_B):
    country_A.name = country_B.name
    with pytest.raises(IntegrityError):
        country_A.save()


def test_country_table_code_constraint(country_A, country_B):
    country_A.code = country_B.code
    with pytest.raises(IntegrityError):
        country_A.save()


def test_activity_table_constraint(activity_A, activity_B):
    activity_A.name = activity_B.name
    with pytest.raises(IntegrityError):
        activity_A.save()
