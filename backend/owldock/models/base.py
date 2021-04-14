import uuid

from django.contrib.contenttypes.models import ContentType
from django.db import models


class BaseModel(models.Model):
    """
    A base class for owldock models.
    """

    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        db_index=True,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
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
            data = self.uuid  # type: ignore
        return f"{data}"
