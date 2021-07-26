"""
This module contains pydantic model definitions, defining the shape of JSON
documents being sent to or received from the javascript app.
"""
from __future__ import annotations
from collections import defaultdict
from decimal import Decimal
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, PositiveInt, NonNegativeInt

from owldock.api.models import DjangoOrmGetterDict
from immigration import models as orm_models


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


class ProcessStepGetterDict(DjangoOrmGetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        # Serialize human-readable label
        if key in {"type"}:
            value = getattr(self._obj, key, default)
            return orm_models.ProcessStepType(value).label if value else None
        else:
            return super().get(key, default)


class ProcessStep(BaseModel):
    id: int
    uuid: UUID
    name: str
    type: str
    host_country: Optional[Country]
    depends_on_ids: List[int]
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
        getter_dict = ProcessStepGetterDict


ProcessStep.update_forward_refs()


class ProcessStepList(BaseModel):
    __root__: List[ProcessStep]

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict

    @classmethod
    def get_orm_models(cls, host_country_code: str) -> List[orm_models.ProcessStep]:
        id2step = _prefetch_process_steps_for_host_country_code(host_country_code)
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
    steps: List[ProcessStep]

    class Config(BaseModel.Config):
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
                "processrulesetstep_set__process_step",
                "nationalities",
                "home_countries",
            )
            .filter(**kwargs)
        )
        if orm_process_rulesets:
            # We do not handle process_rulesets from a mixture of countries.
            [country_code] = {pr.route.host_country.code for pr in orm_process_rulesets}
            id2step = _prefetch_process_steps_for_host_country_code(country_code)
            for pr in orm_process_rulesets:
                for sr in pr.step_rulesets:
                    sr.process_step = id2step[sr.process_step_id]

        return orm_process_rulesets


def _prefetch_process_steps_for_host_country_code(
    country_code: str,
) -> Dict[int, orm_models.ProcessStep]:
    """
    Return available ProcessSteps with related objects prefetched.
    """
    steps = (
        orm_models.ProcessStep.objects.get_for_host_country_codes([country_code])
        .select_related("host_country")
        .prefetch_related(
            "required_only_if_home_country",
            "required_only_if_nationalities",
        )
    )
    id2step = {s.id: s for s in steps}

    # Get dependencies
    id2depends_on_ids: Dict[int, List[int]] = defaultdict(list)
    for from_id, to_id in orm_models.ProcessStep.depends_on.through.objects.filter(
        from_processstep__in=id2step
    ).values_list("from_processstep_id", "to_processstep_id"):
        id2depends_on_ids[from_id].append(to_id)

    # Attach prefetched dependency steps, but only those that are relevant to
    # this country. For example, the Entry step is global and thus may depend on
    # steps in many countries, but we restrict to its dependencies that are
    # steps available in the current country.
    for step in steps:
        step._prefetched_depends_on = [
            id2step[id] for id in id2depends_on_ids[step.id] if id in id2step
        ]

    return id2step
