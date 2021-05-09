from django.db.models import CharField, ManyToManyField

from app.models.country import Country
from owldock.models.base import BaseModel


class Bloc(BaseModel):
    name = CharField(help_text="The name of this bloc", max_length=128)
    countries = ManyToManyField(Country, blank=True)
