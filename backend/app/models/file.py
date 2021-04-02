from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import (
    CharField,
    deletion,
    FileField,
    ForeignKey,
    PositiveIntegerField,
)

from app.models.base import BaseModel


class ApplicationFileType(models.TextChoices):
    PROVIDER_CONTACT_UPLOAD = ("PROVIDER_CONTACT_UPLOAD",)


class StoredFile(BaseModel):
    # {'_name': 'babel.config.js', 'charset': None, 'content_type': 'text/javascript', 'content_type_extra': {}, 'field_name': 'file', 'file': <_io.BytesIO object ...106c56450>, 'size': 66}
    file = FileField(upload_to="uploads/%Y/%m/")
    created_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=deletion.PROTECT)
    application_file_type = CharField(
        max_length=64, choices=ApplicationFileType.choices
    )

    # GFK
    associated_object_content_type = ForeignKey(ContentType, on_delete=deletion.PROTECT)
    associated_object_id = PositiveIntegerField()
    associated_object = GenericForeignKey(
        "associated_object_content_type",
        "associated_object_id",
    )
