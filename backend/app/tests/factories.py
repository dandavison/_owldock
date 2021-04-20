from io import BytesIO

import factory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import UploadedFile
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
    # Invalid, but the constraint is deferred to the end of the transaction.
    primary_contact_id = 0

    @factory.post_generation
    def create_primary_contact(self, create, extracted, **kwargs):
        self.primary_contact = ProviderContactFactory(provider=self)

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


class UploadedFileFactory(factory.Factory):
    class Meta:
        model = UploadedFile

    file = factory.LazyAttribute(lambda obj: BytesIO(b"file-contents"))
    content_type = factory.Faker("mime_type")
    charset = "utf-8"
    name = factory.Faker("file_name")
    size = 777
