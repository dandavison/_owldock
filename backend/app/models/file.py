from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import (
    CharField,
    deletion,
    FileField,
    ForeignKey,
    PositiveIntegerField,
)

from app.models import BaseModel


class FileTypes(models.TextChoices):
    PROVIDER_CONTACT_UPLOAD = ("PROVIDER_CONTACT_UPLOAD",)


class File(BaseModel):
    created_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=deletion.PROTECT)
    type = CharField(max_length=64, choices=FileTypes.choices)
    file = FileField(upload_to="uploads/%Y/%m/")
    content_type = ForeignKey(ContentType, on_delete=deletion.PROTECT)
    object_id = PositiveIntegerField()
