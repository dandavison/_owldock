from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        if hasattr(self, "name"):
            data = self.name  # type: ignore # pylint: disable=no-member
        elif hasattr(self, "user"):
            data = self.user.email  # type: ignore # pylint: disable=no-member
        else:
            data = self.id  # type: ignore
        return f"{data}"
