from uuid import UUID
import random

import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory import Factory, LazyAttribute

from app.models import Country, Provider, ProviderContact, Route
from client.models import Applicant, Client, ClientContact
from owldock.models.base import BaseModel


random.seed("owldock")


class BaseModelFactory(DjangoModelFactory):
    class Meta:
        model = BaseModel
        abstract = True
