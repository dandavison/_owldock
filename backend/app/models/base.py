from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        if hasattr(self, "name"):
            data = self.name  # type: ignore
        elif hasattr(self, "user"):
            data = self.user.email  # type: ignore
        else:
            data = self.id  # type: ignore
        return f"{data}"
