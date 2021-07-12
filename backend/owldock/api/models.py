from typing import Any

import pydantic.utils
from django.db.models import Manager as DjangoModelManager, QuerySet
from djmoney.money import Money


class DjangoOrmGetterDict(pydantic.utils.GetterDict):
    # https://github.com/samuelcolvin/pydantic/pull/2463
    def get(self, key: Any, default: Any = None) -> Any:
        value = super().get(key, default)
        if isinstance(value, (DjangoModelManager, QuerySet)):
            return list(value.all())
        elif isinstance(value, Money):
            return value.amount
        else:
            return value


class BaseModel(pydantic.BaseModel):
    class Config:
        orm_mode = True
        getter_dict = DjangoOrmGetterDict


class EnumValue(BaseModel):
    name: str
    value: str
