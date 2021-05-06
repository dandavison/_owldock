from typing import Type

from parameterized import parameterized
from django.db.models import Model
from django.db import router

from app.models import ProviderContact
from client.models import Applicant, Case
from immigration.models import ProcessRuleSet

from owldock.database_router import is_client_model


@parameterized.expand(
    [
        (Case, "client"),
        (ProcessRuleSet, "default"),
        (ProviderContact, "default"),
    ]
)
def test_db_router(model: Type[Model], db: str):
    assert router.db_for_read(model) == db
    assert router.db_for_write(model) == db


@parameterized.expand(
    [
        ("client", "client", True),
        ("default", "client", False),
        ("client", "app", False),
        ("default", "app", True),
    ]
)
def test_db_router_allow_migrate(db: str, app_label: str, expected: bool):
    assert router.allow_migrate(db, app_label) == expected


@parameterized.expand(
    [
        (Case, Applicant, True),
        (Case, ProviderContact, False),
        (Case, ProcessRuleSet, False),
        (Applicant, ProviderContact, False),
        (Applicant, ProcessRuleSet, False),
        (ProviderContact, ProcessRuleSet, True),
    ]
)
def test_db_router_allow_relation(
    model1: Type[Model], model2: Type[Model], expected: bool
):
    obj1, obj2 = model1(), model2()
    assert router.allow_relation(obj1, obj1)
    assert router.allow_relation(obj2, obj2)
    assert router.allow_relation(obj1, obj2) == expected
    assert router.allow_relation(obj2, obj1) == expected


def test_is_client_model():
    assert is_client_model(Case)
    assert not is_client_model(ProcessRuleSet)
    assert not is_client_model(ProviderContact)
