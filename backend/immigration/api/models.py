"""
This module contains pydantic model definitions, defining the shape of JSON
documents being sent to or received from the javascript app.
"""
from __future__ import annotations
from decimal import Decimal
from operator import itemgetter
from typing import Any, List, Optional
from uuid import UUID

from cytoolz import itertoolz

from django.db.models import Manager as DjangoModelManager
from djmoney.money import Money
from pydantic import BaseModel, PositiveInt, NonNegativeInt
from pydantic.utils import GetterDict

from immigration import models as orm_models


class DjangoOrmGetterDict(GetterDict):
    # https://github.com/samuelcolvin/pydantic/pull/2463
    def get(self, key: Any, default: Any = None) -> Any:
        value = super().get(key, default)
        if isinstance(value, DjangoModelManager):
            return list(value.all())
        elif isinstance(value, Money):
            return value.amount
        else:
            return value


class Country(BaseModel):
    uuid: UUID
    name: str
    code: str
    currency_code: Optional[str]
    unicode_flag: str

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict


class CountryList(BaseModel):
    __root__: List[Country]

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict


class Route(BaseModel):
    name: str
    host_country: Country

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict


class ProcessStep(BaseModel):
    id: int
    name: str
    host_country: Optional[Country]
    depends_on_: List[ProcessStep]
    step_government_fee: Optional[Decimal]
    step_duration_range: List[Optional[int]]
    required_only_if_contract_location: Optional[str]
    required_only_if_payroll_location: Optional[str]
    required_only_if_duration_greater_than: Optional[int]
    required_only_if_duration_less_than: Optional[int]
    required_only_if_nationalities: List[Country]
    required_only_if_home_country: List[Country]

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict


ProcessStep.update_forward_refs()


class ProcessStepList(BaseModel):
    __root__: List[ProcessStep]

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict

    @classmethod
    def get_orm_models(cls, host_country_code: str) -> List[orm_models.ProcessStep]:
        id2step = _prefetch_process_steps_for_host_country_codes([host_country_code])
        return list(id2step.values())


class ProcessStepRuleSet(BaseModel):
    # id: int
    process_step: ProcessStep

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict


class ProcessRuleSetGetterDict(DjangoOrmGetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        # Serialize human-readable labels of these enums
        if key in {"contract_location", "payroll_location"}:
            value = getattr(self._obj, key, default)
            return orm_models.Location(value).label if value else None
        else:
            return super().get(key, default)


class ProcessRuleSet(BaseModel):
    id: int
    uuid: UUID
    route: Route
    nationalities: List[Country]
    home_countries: List[Country]
    contract_location: Optional[str]
    payroll_location: Optional[str]
    minimum_salary: Optional[Decimal]
    minimum_salary_currency: Optional[str]
    duration_min_days: Optional[NonNegativeInt]
    duration_max_days: Optional[PositiveInt]
    intra_company_moves_only: bool
    nationalities_description = ""  # computed in HTTP handler
    step_rulesets: List[ProcessStepRuleSet]

    class Config:
        orm_mode = True
        getter_dict = ProcessRuleSetGetterDict

    @classmethod
    def get_orm_model(cls, **kwargs) -> orm_models.ProcessRuleSet:
        [process_ruleset] = ProcessRuleSetList.get_orm_models(**kwargs)
        return process_ruleset


class ProcessRuleSetList(BaseModel):
    __root__: List[ProcessRuleSet]

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict

    @classmethod
    def get_orm_models(cls, **kwargs) -> List[orm_models.ProcessRuleSet]:
        """
        Return ProcessRuleSet `id`, with all related objects prefetched such
        that no queries are made during subsequent serialization.
        """
        orm_process_rulesets = list(
            orm_models.ProcessRuleSet.objects.select_related(
                "route__host_country",
            )
            .prefetch_related(
                "processrulesetstep_set",
                "nationalities",
                "home_countries",
            )
            .filter(**kwargs)
        )
        id2step = _prefetch_process_steps_for_host_country_codes(
            [pr.route.host_country.code for pr in orm_process_rulesets]
        )
        for pr in orm_process_rulesets:
            for sr in pr.step_rulesets:
                sr.process_step = id2step[sr.process_step_id]

        return orm_process_rulesets


def _prefetch_process_steps_for_host_country_codes(country_codes: List[str]):
    # Create a pool of ProcessStep instances with all related objects
    # prefetched.
    id2step = (
        orm_models.ProcessStep.objects.get_for_host_country_codes(country_codes)
        .select_related("host_country")
        .prefetch_related(
            "required_only_if_nationalities",
            "required_only_if_home_country",
        )
        .in_bulk()
    )
    id2depends_on_ids = itertoolz.groupby(
        itemgetter(0),
        (
            orm_models.ProcessStep.depends_on.through.objects.filter(
                from_processstep__in=id2step
            ).values_list("from_processstep_id", "to_processstep_id")
        ),
    )
    for process_step in id2step.values():
        process_step._prefetched_depends_on = [
            id2step[id]
            for _, id in id2depends_on_ids.get(id, [])
            # id will not be in id2step if sr.process_step_id is a
            # global step and id is a step in a different country.
            if id in id2step
        ]
    return id2step
