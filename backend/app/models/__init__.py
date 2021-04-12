import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        db_index=True,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


from app.models.process import *  # noqa
from app.models.provider import *  # noqa
