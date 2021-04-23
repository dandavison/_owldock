from uuid import UUID
import random

import factory
from factory.django import DjangoModelFactory
from factory import Factory, LazyAttribute

from app.models import Country
from app.tests.factories import create_user
from client.models import Applicant, Client, ClientContact
from owldock.tests.factories import BaseModelFactory


def UUIDPseudoForeignKeyFactory(_factory: Factory, to_field="uuid") -> LazyAttribute:
    def _get_uuid(_) -> UUID:
        to_value = getattr(_factory(), to_field)
        assert isinstance(to_value, UUID)
        return to_value

    return factory.LazyAttribute(_get_uuid)


class _HasUserUUIDFactory(BaseModelFactory):
    """
    An owldock model, inheriting from BaseModel, with a UUID link to auth.User.
    """

    class Meta:
        abstract = True

    user_uuid = UUIDPseudoForeignKeyFactory(create_user, to_field="uuid")


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client
        database = "client"

    name = factory.Faker("company")
    entity_domain_name = factory.LazyAttribute(lambda obj: f"{obj.name}.com")
    logo_url = factory.Faker("url")


class ApplicantFactory(_HasUserUUIDFactory):
    class Meta:
        model = Applicant
        database = "client"

    employer = factory.SubFactory(ClientFactory)
    home_country_uuid = factory.LazyAttribute(
        lambda _: random.choice(list(Country.objects.all())).uuid
    )


class ClientContactFactory(_HasUserUUIDFactory):
    class Meta:
        model = ClientContact
        database = "client"

    client = factory.SubFactory(ClientFactory)
