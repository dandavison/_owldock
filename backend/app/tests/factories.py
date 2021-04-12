from uuid import UUID

import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from factory import Factory, LazyAttribute

from app.models import Country, Provider, ProviderContact, Route
from client.models import Applicant, Client, ClientContact
from owldock.models import BaseModel


class BaseModelFactory(DjangoModelFactory):
    class Meta:
        model = BaseModel
        abstract = True


def UUIDPseudoForeignKeyFactory(factory_cls: Factory, to_field="id") -> LazyAttribute:
    def _get_uuid(_) -> UUID:
        to_value = getattr(factory_cls(), to_field)
        assert isinstance(to_value, UUID)
        return to_value

    return factory.LazyAttribute(_get_uuid)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()

    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")

    @factory.iterator
    def username():  # noqa
        n = get_user_model().objects.filter(username__startswith="user_").count()
        while True:
            yield f"user_{n}"
            n = n + 1


class _HasUserFactory(BaseModelFactory):
    """
    An owldock model, inheriting from BaseModel, with a UUID link to auth.User.
    """

    class Meta:
        abstract = True

    user_id = UUIDPseudoForeignKeyFactory(UserFactory, to_field="uuid")


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client
        database = "client"

    name = factory.Faker("company")
    entity_domain_name = factory.LazyAttribute(lambda obj: f"{obj.name}.com")
    logo_url = factory.Faker("url")


class ApplicantFactory(_HasUserFactory):
    class Meta:
        model = Applicant
        database = "client"

    employer = factory.SubFactory(ClientFactory)
    home_country_id = factory.Iterator(Country.objects.all(), getter=lambda c: c.id)


class ClientContactFactory(_HasUserFactory):
    class Meta:
        model = ClientContact
        database = "client"

    client = factory.SubFactory(ClientFactory)


class ProviderFactory(DjangoModelFactory):
    class Meta:
        model = Provider

    name = factory.Faker("company")
    logo_url = factory.Faker("url")

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for route_name in extracted:
                self.routes.add(Route.objects.get(name=route_name))


class ProviderContactFactory(_HasUserFactory):
    class Meta:
        model = ProviderContact

    provider = factory.SubFactory(ProviderFactory)
