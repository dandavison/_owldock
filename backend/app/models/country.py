# Regarding use of Meta.constraints rather than unique=True in the field
# declaration:
# Suppose some POST data has been received by a DRF serializer, and the plan is
# to create Service entries with get_or_create semantics. The DRF serializer
# will fail its validity check if the new Service entries look like they are
# going to try to create duplicates. But only if the unique_contraint is added
# in the Django field definition.
from django.db import models

from owldock.models.base import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=2)
    unicode_flag = models.CharField(max_length=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("name",),
                name="country__name__unique_constraint",
            ),
            models.UniqueConstraint(
                fields=("code",), name="country__code__unique_constraint"
            ),
        ]
        verbose_name_plural = "Countries"
