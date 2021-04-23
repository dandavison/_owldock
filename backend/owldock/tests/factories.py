import random

from factory.django import DjangoModelFactory

from owldock.models.base import BaseModel


random.seed("owldock")


class BaseModelFactory(DjangoModelFactory):
    class Meta:
        model = BaseModel
        abstract = True
