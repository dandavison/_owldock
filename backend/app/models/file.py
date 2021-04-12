from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django.db.models import (
    CharField,
    deletion,
    FileField,
    ForeignKey,
    PositiveIntegerField,
    UUIDField,
)

from owldock.models import BaseModel


class ApplicationFileType(models.TextChoices):
    PROVIDER_CONTACT_UPLOAD = ("PROVIDER_CONTACT_UPLOAD",)


class StoredFile(BaseModel):
    # File attributes
    file = FileField(upload_to="uploads/%Y/%m/")
    name = CharField(max_length=256)
    media_type = CharField(max_length=128)
    size = PositiveIntegerField()
    charset = CharField(max_length=8, null=True)

    # Application attributes
    application_file_type = CharField(
        max_length=64, choices=ApplicationFileType.choices
    )
    # Not actually using a Django GFK due to our multiple database setup
    associated_object_content_type = ForeignKey(ContentType, on_delete=deletion.PROTECT)
    associated_object_id = UUIDField()

    @classmethod
    def from_uploaded_file(cls, uploaded_file: UploadedFile) -> "StoredFile":
        return StoredFile(
            file=uploaded_file,
            media_type=uploaded_file.content_type or "",
            charset=uploaded_file.charset,
            name=uploaded_file.name,
            size=uploaded_file.size,
        )
