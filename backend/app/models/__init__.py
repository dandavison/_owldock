import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from owldock.api.http.utils import get_current_user_uuid
from owldock.models.fields import UUIDPseudoForeignKeyField


class User(AbstractUser):
    # TODO: these field definitions are duplicated in BaseModel.
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        db_index=True,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_id = UUIDPseudoForeignKeyField(
        "User",
        null=True,
        default=lambda: get_current_user_uuid,
        to_field="uuid",
    )
    modified_at = models.DateTimeField(auto_now=True)


from app.models.process import *  # noqa
from app.models.provider import *  # noqa
