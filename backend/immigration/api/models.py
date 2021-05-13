"""
This module contains pydantic model definitions, defining the shape of JSON
documents being sent to or received from the javascript app.
"""
from decimal import Decimal
from typing import Any, List, Optional

from django.db.models import Manager as DjangoModelManager
from pydantic import BaseModel, PositiveInt
from pydantic.utils import GetterDict


class DjangoOrmGetterDict(GetterDict):
    # https://github.com/samuelcolvin/pydantic/pull/2463
    def get(self, *args, **kwargs) -> Any:
        value = super().get(*args, **kwargs)
        if isinstance(value, DjangoModelManager):
            return list(value.all())
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


class ProcessRuleSet(BaseModel):
    route: Route
    nationalities: List[Country]
    home_countries: List[Country]
    contract_location: Optional[str]
    payroll_location: Optional[str]
    minimum_salary: Optional[Decimal]
    duration_min_days: Optional[PositiveInt]
    duration_max_days: Optional[PositiveInt]
    intra_company_moves_only: bool

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict


class ProcessRuleSetList(BaseModel):
    __root__: List[ProcessRuleSet]

    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict
