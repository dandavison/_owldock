import uuid

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models

from owldock.api.http.utils import get_current_user_uuid
from owldock.models.fields import UUIDPseudoForeignKeyField


class BaseModel(models.Model):
    """
    A base class for owldock models.
    """

    # We use UUID primary keys instead of the familiar auto-incrementing
    # integers. The reason is that our tables are split across multiple
    # databases (tables holding client data fields are in a different database
    # from tables holding non-client data fields), so in several cases where we
    # would want a foreign key, we cannot use one, instead storing a unique
    # identifier without the referential integrity guarantee of a true FK. UUIDs
    # are an appropriate choice for such unique identifiers. Rather than have
    # some tables with integer 'id' primary keys only, and some with integer
    # 'id' primary key and UUID, we elect to just use UUID primary keys on all
    # tables. We name the UUID primary key 'id'.
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_index=True,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_id = UUIDPseudoForeignKeyField(
        settings.AUTH_USER_MODEL,
        null=True,
        default=lambda: get_current_user_uuid,
        to_field="uuid",
    )
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.__class__)

    def __str__(self) -> str:
        if hasattr(self, "name"):
            data = self.name  # type: ignore
        elif hasattr(self, "user"):
            data = self.user.email  # type: ignore
        else:
            data = self.id  # type: ignore
        return f"{data}"
