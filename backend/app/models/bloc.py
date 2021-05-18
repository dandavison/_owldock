from collections import defaultdict
from typing import Callable, Dict, Iterable, List, Tuple

from django.db.models import CharField, Manager, ManyToManyField

from app.models.country import Country
from owldock.models.base import BaseModel
from owldock.utils.set_decomposer import SetDecomposer

# Maximum value of n for `bloc + n` to be a valid description of a set of countries.
MAX_ADDITIONAL_COUNTRIES = 10


class BlocManager(Manager):
    def make_get_description_from_countries(
        self,
    ) -> "Callable[[Iterable[Country]], str]":
        """
        Return a function taking as input an iterable of countries and returning
        a string describing the set of countries in terms of blocs.
        """
        bloc_names2country_codes = {
            b.name: [c.code for c in b.countries.all()]
            for b in Bloc.objects.prefetch_related("countries")
        }
        all_country_codes = set(Country.objects.values_list("code", flat=True))
        decomposer = SetDecomposer(bloc_names2country_codes, all_country_codes)

        return lambda countries: decomposer.decompose([c.code for c in countries])

    def get_country_id2containing_blocs(self) -> "Dict[int, List[Bloc]]":
        """
        Return map of country-id to list-of-blocs-containing-that-country
        """
        bloc_id2bloc = {b.id: b for b in Bloc.objects.all()}
        country_id2containing_blocs = defaultdict(list)
        for bloc_id, country_id in Bloc.countries.through.objects.values_list(
            "bloc_id", "country_id"
        ):
            country_id2containing_blocs[country_id].append(bloc_id2bloc[bloc_id])
        return dict(country_id2containing_blocs)


class Bloc(BaseModel):
    name = CharField(help_text="The name of this bloc", max_length=128)
    countries = ManyToManyField(Country, blank=True)

    objects = BlocManager()
