"""
This module contains pydantic model definitions, defining the shape of JSON
documents being sent to or received from the javascript app.
"""
from decimal import Decimal
from typing import Any, List, Optional
from uuid import UUID

from django.db.models import Manager as DjangoModelManager
from djmoney.money import Money
from pydantic import BaseModel, PositiveInt, NonNegativeInt
from pydantic.utils import GetterDict

from immigration.models import Location


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
    name: str
    code: str
    unicode_flag: str

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict


class Route(BaseModel):
    name: str
    host_country: Country

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict


class ProcessRuleSetGetterDict(DjangoOrmGetterDict):
    def get(self, key: Any, default: Any = None) -> Any:
        # Serialize human-readable labels of these enums
        if key in {"contract_location", "payroll_location"}:
            value = getattr(self._obj, key, default)
            return Location(value).label if value else None
        else:
            return super().get(key, default)


class ProcessRuleSet(BaseModel):
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

    class Config:
        orm_mode = True
        getter_dict = ProcessRuleSetGetterDict


class ProcessRuleSetList(BaseModel):
    __root__: List[ProcessRuleSet]

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict
