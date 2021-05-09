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
    # TODO: what is the role of the username field?
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("email",), name="user__email__unique_constraint"
            )
        ]


from app.models.bloc import Bloc
from app.models.country import *  # noqa
from app.models.file import *  # noqa
from app.models.provider import *  # noqa
