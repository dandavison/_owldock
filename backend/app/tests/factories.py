import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from app.models import Activity, Provider, ProviderContact, Route
from owldock.tests.factories import BaseModelFactory


class ActivityFactory(DjangoModelFactory):
    class Meta:
        model = Activity

    name = factory.Faker("job")


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
    An owldock model, inheriting from BaseModel, with a foreign key to auth.User.
    """

    class Meta:
        abstract = True

    user = factory.SubFactory(UserFactory)


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
